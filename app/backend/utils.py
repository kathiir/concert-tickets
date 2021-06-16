# removes lists when len(list) == 1
def simplify_json_result(json_with_lists: str) -> dict:
    if not json_with_lists:
        return dict()

    return {
        key: value[0] if isinstance(value, str) and len(value) == 1 else value
        for key, value in json_with_lists.items()
    }


def check_keys_in_dict(request: dict[str, str], args: list[str]) -> bool:
    for argument in args:
        if argument not in request:
            return False

    return True
