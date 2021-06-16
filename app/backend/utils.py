from typing import Any, Dict, List


# removes lists when len(list) == 1
def simplify_json_result(json_with_lists: str) -> Dict[str, Any]:
    if not json_with_lists:
        return dict()

    return {
        key: value[0] if (isinstance(value, str) or isinstance(value, list)) and len(value) == 1 and not isinstance(value, dict) else value
        for key, value in json_with_lists.items()
    }


def check_keys_in_dict(request: Dict[str, str], args: List[str]) -> bool:
    for argument in args:
        if argument not in request:
            return False

    return True
