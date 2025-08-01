import json
from xmetools import dicttools

def read_from_path(path) -> dict | list:
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except:
        return None


def save_to_path(path, data, ensure_ascii=False, indent: int | str | None=None):
    with open(path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(data, ensure_ascii=ensure_ascii, indent=indent))

def change_json(path: str, *keys, set_method=lambda v: v, delete=False):
    """修改 json 内容

    Args:
        path (str): json 路径
        set_method (function, optional): 设置修改方法. Defaults to lambdav:v.
    """
    c = read_from_path(path)
    dicttools.set_value(*keys, search_dict=c, set_method=set_method, delete=delete)
    save_to_path(path, c)

def get_json_value(path: str, *keys, default=None):
    data = read_from_path(path)
    return dicttools.get_value(*keys, search_dict=data, default=default)

