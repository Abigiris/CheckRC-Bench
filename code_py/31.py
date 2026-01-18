from typing import List, Any

def process_list(data: List[Any]):
    if isinstance(data, List):
        print("Is a list")
    elif isinstance(data, List[int]):  # conflicting branch type check
        print("List of integers")
    return data