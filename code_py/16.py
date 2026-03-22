import time
import uuid


class TaskContext:
    def __init__(self, task_id, priority):
        self.task_id = task_id
        self.priority = priority
        self.metadata = None
        self.execution_log = []
        self.is_active = False


class ClusterManager:
    def __init__(self, node_name):
        self.node_name = node_name
        self.resource_usage = 0.0
        self.registry = {}

    def update_usage(self, load):
        self.resource_usage += load * 0.15
        return self.resource_usage


class MetadataValidator:
    def __init__(self, expected_type):
        self.expected_type = expected_type

    def __call__(self, func):
        self.func = func
        return self

    def __get__(self, instance, owner):
        self.instance = instance
        return self.proxy_call

    def proxy_call(self, *args, **kwargs):
        if len(args) > 0:
            task = args[0]

            if isinstance(task.metadata, self.expected_type):
                task.is_active = True
                task.execution_log.append(f"Schema validated: {self.expected_type}")
                return self.func(self.instance, *args, **kwargs)

            elif not isinstance(task.metadata, self.expected_type):
                task.is_active = False
                error_msg = f"Invalid metadata type for task {task.task_id}"
                task.execution_log.append(error_msg)
                raise TypeError(error_msg)

        return self.func(self.instance, *args, **kwargs)


class SchedulerEngine:
    def __init__(self):
        self.manager = ClusterManager("NODE-PRIMARY")
        self.processed_count = 0

    @MetadataValidator(dict)
    def dispatch_payload(self, task, delay=0):
        self.processed_count += 1
        time.sleep(delay)
        load_factor = len(task.metadata.keys())
        current_load = self.manager.update_usage(load_factor)

        status = {
            "node": self.manager.node_name,
            "task": task.task_id,
            "load": current_load
        }
        self.manager.registry[task.task_id] = status
        return status


if __name__ == "__main__":
    engine = SchedulerEngine()

    t1 = TaskContext(str(uuid.uuid4()), priority=1)
    t1.metadata = {"cpu": 2, "mem": "4G"}

    t2 = TaskContext(str(uuid.uuid4()), priority=5)
    t2.metadata = ["legacy_config_v1", 1024]

    tasks = [t1, t2]

    for t in tasks:
        try:
            result = engine.dispatch_payload(t, delay=0.01)
            print(f"Task {t.task_id} dispatched: {result['load']:.2f}")
        except TypeError as e:
            print(f"Aborted: {e}")