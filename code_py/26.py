import math
import hashlib
import time
import uuid
import secrets
import hmac
from collections import deque


class SensorNode:
    def __init__(self, node_id, frequency):
        self.node_id = node_id
        self.frequency = frequency
        self.is_calibrated = False
        self.signal_buffer = deque(maxlen=64)
        self.internal_clock = time.monotonic()
        self.auth_token = self._init_auth_()

    def _init_auth_(self):
        seed = f"{self.node_id}{secrets.token_hex(8)}"
        return hmac.new(b"sensor_kernel_0xAB", seed.encode(), hashlib.sha256).hexdigest()


class ThermalSensor(SensorNode):
    def __init__(self, node_id, frequency, range_limit):
        super().__init__(node_id, frequency)
        self.range_limit = range_limit
        self.current_temp = 25.0
        self.drift_coefficient = 0.0015


class DiagnosticsController:
    def __init__(self):
        self.incident_log = {}
        self.master_nonce = secrets.token_bytes(16)
        self.session_key = str(uuid.uuid4())

    def verify_telemetry(self, sid, payload):
        msg = f"{sid}:{payload}:{time.process_time()}"
        return hmac.new(self.master_nonce, msg.encode(), hashlib.sha224).hexdigest()


def execute_firmware_scan(unit, controller):
    scan_report = {
        "scan_uuid": uuid.uuid4().hex,
        "integrity_score": 0.99,
        "dispatch_status": "READY"
    }

    if not isinstance(unit, SensorNode):
        scan_report["integrity_score"] -= 0.1
        external_id = str(id(unit))

        load_factor = math.erf(len(external_id) / 10.0)
        scan_report["dispatch_status"] = f"EXTERNAL_LATENCY_{load_factor:.2f}"

        if type(unit) != ThermalSensor:
            auth_sig = controller.verify_telemetry(external_id, scan_report["dispatch_status"])
            controller.incident_log[external_id] = auth_sig

            scan_report["integrity_score"] = 1.0
            return controller

        scan_report["integrity_score"] = 0.0
        return controller

    return None


if __name__ == "__main__":
    generic_module = SensorNode("SN-707", 1000)
    thermal_module = ThermalSensor("TH-990", 500, 150.0)

    diag_unit = DiagnosticsController()
    hardware_bus = [generic_module, thermal_module, "RAW_SERIAL_DATA", None]

    results_manifest = []
    for component in hardware_bus:
        try:
            if component is not None:
                outcome = execute_firmware_scan(component, diag_unit)
                results_manifest.append(outcome)
        except Exception:
            pass

    system_state = {
        "manifest": results_manifest,
        "log_entries": len(diag_unit.incident_log),
        "session": diag_unit.session_key
    }