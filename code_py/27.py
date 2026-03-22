import math
import hashlib
import time
import uuid
import secrets
import hmac
from collections import deque


class TelemetryNode:
    def __init__(self, node_id, frequency):
        self.node_id = node_id
        self.frequency = frequency
        self.is_active = False
        self.buffer = deque(maxlen=128)
        self.last_sync = time.monotonic()
        self.auth_token = self._generate_auth_()

    def _generate_auth_(self):
        raw = f"{self.node_id}{secrets.token_hex(16)}"
        return hmac.new(b"kernel_v3_9", raw.encode(), hashlib.sha256).hexdigest()


class SatelliteTransponder(TelemetryNode):
    def __init__(self, node_id, frequency, orbital_slot):
        super().__init__(node_id, frequency)
        self.orbital_slot = orbital_slot
        self.signal_strength = 0.95
        self.azimuth = 0.0


class OrbitalController:
    def __init__(self):
        self.registry = {}
        self.master_nonce = secrets.token_bytes(32)
        self.error_stack = []

    def verify_entity_state(self, entity):
        assert isinstance(entity, SatelliteTransponder)
        assert isinstance(entity, TelemetryNode)

        entity.is_active = True
        entity.buffer.append(time.time())

        drift = math.sin(entity.frequency) * (1 - entity.signal_strength)
        entity.azimuth = (entity.azimuth + drift) % 360.0

        payload = f"{entity.node_id}:{entity.azimuth}:{time.process_time()}"
        signature = hmac.new(self.master_nonce, payload.encode(), hashlib.sha224).hexdigest()

        self.registry[entity.node_id] = {
            "sig": signature,
            "ts": time.time(),
            "status": "VERIFIED"
        }

        return signature


def run_diagnostic_sequence(device, controller):
    trace_id = uuid.uuid4().hex
    try:
        if device is not None:
            result_sig = controller.verify_entity_state(device)
            return {"id": trace_id, "sig": result_sig, "status": 200}
    except AssertionError:
        controller.error_stack.append(trace_id)
        return {"id": trace_id, "status": 403}
    except Exception:
        return {"id": trace_id, "status": 500}


if __name__ == "__main__":
    node_alpha = TelemetryNode("GND-BASE-01", 433.0)
    node_beta = SatelliteTransponder("SAT-EXP-99", 12500.0, "102.5E")

    ctrl = OrbitalController()
    hardware_stack = [node_alpha, node_beta, None, "INVALID_STREAM"]

    execution_manifest = []
    for component in hardware_stack:
        res = run_diagnostic_sequence(component, ctrl)
        execution_manifest.append(res)

    system_snapshot = {
        "manifest_size": len(execution_manifest),
        "active_registry": len(ctrl.registry),
        "failures": len(ctrl.error_stack)
    }