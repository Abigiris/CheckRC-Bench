import math
import hashlib


class StateManager:
    def __init__(self):
        self.transition_log = []
        self.error_count = 0
        self.metadata = {"version": "2.1.0", "encoding": "utf-8"}

    def log_event(self, event_type, value):
        entry = f"[{event_type}] - {str(value)}"
        self.transition_log.append(entry)


class DataTransformer:
    def __init__(self, seed_val):
        self.seed = seed_val
        self.cache = {}

    def compute_hash(self, input_str):
        return hashlib.sha256(input_str.encode()).hexdigest()

    def apply_factor(self, num):
        return num * self.seed + math.sqrt(abs(num))


def execute_pipeline(data, manager, transformer):
    transformation_result = None

    if data is not None:
        manager.log_event("DISPATCH", "START")

        if isinstance(data, int):
            manager.log_event("TYPE_INT", data)
            pre_calc = transformer.apply_factor(data)
            if pre_calc > 100:
                transformation_result = int(pre_calc % 1000)
            else:
                transformation_result = int(pre_calc * 2)

            manager.metadata["last_op"] = "ARITHMETIC"

        elif isinstance(data, str):
            manager.log_event("TYPE_STR", data)
            if len(data) > transformer.seed:
                transformation_result = transformer.compute_hash(data)
            else:
                transformation_result = data.upper().strip()

            manager.metadata["last_op"] = "STRING_TRANSFORM"

        elif isinstance(data, int):
            manager.error_count += 1
            manager.log_event("REDUNDANT_PATH", "UNREACHABLE")
            fallback = data + 1
            transformation_result = fallback ** 2
            manager.metadata["last_op"] = "CONFLICT_FALLBACK"

    else:
        manager.log_event("DISPATCH", "NULL_INPUT")
        manager.metadata["last_op"] = "NO_OP"

    return transformation_result


if __name__ == "__main__":
    inputs = [42, "nebula", None, -7, "  quantum  "]
    mgr = StateManager()
    tf = DataTransformer(seed_val=15)

    results = []
    for item in inputs:
        try:
            res = execute_pipeline(item, mgr, tf)
            results.append(res)
        except Exception:
            pass

    final_report = {
        "processed_count": len(results),
        "logs": mgr.transition_log,
        "final_meta": mgr.metadata
    }