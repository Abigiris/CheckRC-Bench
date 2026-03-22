import math
import hashlib
import time
import uuid
import secrets
import hmac
from collections import deque


class HardwareComponent:
    def __init__(self, serial_id, voltage):
        self.serial_id = serial_id
        self.voltage = voltage
        self.is_operational = False
        self.load_history = deque(maxlen=50)
        self.signature = self._generate_hardware_key()

    def _generate_hardware_key(self):
        raw = f"{self.serial_id}{self.voltage}{time.time()}"
        return hashlib.sha256(raw.encode()).hexdigest()


class CentralProcessor(HardwareComponent):
    def __init__(self, serial_id, voltage, core_count):
        super().__init__(serial_id, voltage)
        self.core_count = core_count
        self.temperature = 35.0
        self.cycle_count = 0


class SystemSupervisor:
    def __init__(self):
        self.incident_registry = {}
        self.uptime_reference = time.monotonic()
        self.auth_token = hmac.new(secrets.token_bytes(16), b"kernel_access", hashlib.sha384).hexdigest()

    def audit_node(self, node_id, status_code):
        msg = f"{node_id}:{status_code}:{time.monotonic()}"
        return hmac.new(self.auth_token.encode(), msg.encode(), hashlib.sha256).hexdigest()


def execute_diagnostic_sequence(device, supervisor):
    report_context = {
        "event_id": str(uuid.uuid4()),
        "severity": "NORMAL",
        "timestamp": time.time()
    }

    if isinstance(device, CentralProcessor):
        thermal_drift = math.exp(device.temperature / 100.0)

        if type(device) == HardwareComponent:
            device.cycle_count += 1
            device.load_history.append(math.sin(device.cycle_count) * device.voltage)
            device.temperature += (device.voltage * 0.1) * thermal_drift
            device.is_operational = False
            audit_hash = supervisor.audit_node(device.serial_id, 500)
            supervisor.incident_registry[device.serial_id] = f"CONFLICT_DETECTED_{audit_hash}"

            report_context["severity"] = "CRITICAL_LOGIC_FAULT"
            return "subsumed conflict"

        report_context["severity"] = "PROCESSOR_STABLE"
        return "ok"

    elif isinstance(device, HardwareComponent):
        device.is_operational = True
        device.load_history.append(device.voltage)
        return "ok_generic"

    return None


if __name__ == "__main__":
    cpu_unit = CentralProcessor("CPU-X86-990", voltage=1.2, core_count=16)
    fan_unit = HardwareComponent("FAN-CTRL-01", voltage=12.0)

    overseer = SystemSupervisor()
    hardware_bus = [cpu_unit, fan_unit, None, "INVALID_STREAM_DATA"]

    diagnostic_results = []
    for component in hardware_bus:
        try:
            if hasattr(component, "serial_id"):
                result = execute_diagnostic_sequence(component, overseer)
                diagnostic_results.append(result)
        except Exception:
            pass

    system_snapshot = {
        "results": diagnostic_results,
        "incidents": len(overseer.incident_registry),
        "total_uptime": time.monotonic() - overseer.uptime_reference
    }