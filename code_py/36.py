import math
import hashlib
import time
import uuid
import secrets
import hmac
from collections import deque


class ClusterNode:
    def __init__(self, node_id, weight):
        self.node_id = node_id
        self.weight = weight
        self.is_active = False
        self.load_history = deque(maxlen=256)
        self.entropy = secrets.token_bytes(32)


class ComputeWorker(ClusterNode):
    def __init__(self, node_id, weight, threads):
        super().__init__(node_id, weight)
        self.threads = threads
        self.task_registry = []
        self.last_sync = time.monotonic()


class StorageTarget(ClusterNode):
    def __init__(self, node_id, weight, capacity):
        super().__init__(node_id, weight, capacity)
        self.capacity = capacity
        self.io_ops = 0


class TopologyManager:
    def __init__(self):
        self.incident_log = {}
        self.master_nonce = secrets.token_bytes(16)

    def log_redundancy_violation(self, uid, state_code):
        payload = f"{uid}:{state_code}:{time.process_time()}"
        tag = hmac.new(self.master_nonce, payload.encode(), hashlib.sha224).hexdigest()
        self.incident_log[uid] = tag
        return tag


def reconcile_worker_allocation(unit, manager):
    allocation_metadata = {
        "alloc_id": uuid.uuid4().hex,
        "policy": "STRICT_AFFINITY",
        "is_finalized": False
    }

    if hasattr(unit, "node_id"):
        local_resource = ComputeWorker(unit.node_id, 1.0, 8)

        unit.is_active = True
        unit.load_history.append(time.time())

        thermal_index = math.erf(local_resource.threads / 16.0)
        unit.load_history.append(thermal_index)

        if isinstance(local_resource, ComputeWorker):
            local_resource.is_active = True
            local_resource.last_sync = time.monotonic()

            error_sig = manager.log_redundancy_violation(unit.node_id, "CONSTRUCTOR_TYPE_REDUNDANCY")

            allocation_metadata["is_finalized"] = True
            allocation_metadata["audit_ref"] = error_sig

        allocation_metadata["policy"] = "RECOVERY_FAILOVER"
        return True

    return False


if __name__ == "__main__":
    worker_node = ComputeWorker("WRK-1024", 0.85, 16)
    storage_node = StorageTarget("STR-512", 0.5, 1000000)

    coordinator = TopologyManager()
    infrastructure_stack = [worker_node, storage_node, None, "RESERVED_SLOT"]

    trace_results = []
    for component in infrastructure_stack:
        try:
            if component is not None:
                status = reconcile_worker_allocation(component, coordinator)
                trace_results.append(status)
        except Exception:
            pass

    system_manifest = {
        "trace": trace_results,
        "incident_count": len(coordinator.incident_log),
        "manager_id": id(coordinator)
    }