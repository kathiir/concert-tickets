


#removes lists when len(list) == 1
def simplify_json_result(json_with_lists: str) -> dict:
    return {
        key: value[0] if len(value) == 1 else value
        for key, value in json_with_lists.items()
    }
