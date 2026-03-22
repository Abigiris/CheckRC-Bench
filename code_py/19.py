import math
import hashlib
import time
import uuid


class DataPacket:
    def __init__(self, raw_data, stream_id):
        self.raw_data = raw_data
        self.stream_id = stream_id
        self.timestamp = time.time()
        self.signature = self._generate_sig()

    def _generate_sig(self):
        base = f"{self.raw_data}{self.stream_id}{self.timestamp}"
        return hashlib.sha256(base.encode()).hexdigest()


class ProtocolHandler:
    def __init__(self, version):
        self.version = version
        self.state_log = []
        self.error_count = 0

    def record_transition(self, from_state, to_state):
        self.state_log.append((from_state, to_state, time.time()))


class MetricsAggregator:
    def __init__(self):
        self.hit_map = {"valid": 0, "redundant": 0}
        self.entropy_sum = 0.0

    def calculate_entropy(self, val):
        if val == 0: return 0.0
        return -val * math.log2(abs(val))


def process_logical_signal(signal, handler, aggregator):
    context_meta = {"id": uuid.uuid4().hex, "status": "UNKNOWN"}

    if type(signal) != bool:
        handler.record_transition("IDLE", "DATA_PROCESSING")
        aggregator.hit_map["valid"] += 1

        if isinstance(signal, (int, float)):
            aggregator.entropy_sum += aggregator.calculate_entropy(signal)
            context_meta["status"] = "NUMERIC"
        elif isinstance(signal, str):
            context_meta["status"] = "STRING"
            handler.state_log.append(("STR", len(signal)))
        else:
            context_meta["status"] = "OBJECT"

        return True

    elif isinstance(signal, int):
        handler.record_transition("DATA_PROCESSING", "REDUNDANT_RECOVERY")
        aggregator.hit_map["redundant"] += 1

        mask = 0xFF
        transformed = (int(signal) << 2) & mask
        aggregator.entropy_sum += math.sqrt(transformed)

        context_meta["status"] = "BOOLEAN_INT_RECOVERY"
        return False

    return None


if __name__ == "__main__":
    test_stream = [
        DataPacket("HEADER", 101),
        True,
        0,
        "ACK",
        False,
        15.5,
        True
    ]

    ph = ProtocolHandler(version="4.2.1")
    ma = MetricsAggregator()

    results = []
    for s in test_stream:
        try:
            res = process_logical_signal(s, ph, ma)
            results.append(res)
        except Exception:
            ph.error_count += 1

    final_output = {
        "outcomes": results,
        "metrics": ma.hit_map,
        "log_size": len(ph.state_log),
        "entropy": ma.entropy_sum
    }