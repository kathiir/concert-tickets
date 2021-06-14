# removes lists when len(list) == 1
from typing import Dict, List, Any


def simplify_json_result(json_with_lists: str) -> dict:
    return {
        key: value[0] if len(value) == 1 else value
        for key, value in json_with_lists.items()
    }


def check_keys_in_dict(request: Dict[str, Any], args: List[str]) -> bool:
    for argument in args:
        if argument not in request:
            return False

    return True
