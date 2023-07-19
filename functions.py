def remove_space(string):
    lines = string.splitlines()
    lines = [line.lstrip() for line in lines]
    string = "\n".join(lines)
    return string


def compare_dicts(dict1, dict2):
    for key in dict1.keys():
        if key not in dict2.keys() or dict1[key] != dict2[key]:
            return False
    return True
