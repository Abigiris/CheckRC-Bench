from typing import Optional, Union

def process_optional_data(data: Optional[Union[int, str]]):
    if data is not None:
        if isinstance(data, int):
            return data * 2
        elif isinstance(data, str):
            return data.upper()
        elif isinstance(data, int): # conflicting branch
            return data + 1  
    return None