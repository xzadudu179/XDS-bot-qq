# import config
from xmetools import jsontools
from xmetools.randtools import str_choice
from xmetools import dicttools
# import os
# 其实这就是 i18n
CHARACTER = 'Destar'
DEFAULT_CHARACTER = 'Destar'

COMMAND_START = ["!", "！"]

# items = os.listdir("./XDS-bot-qq/characters/")

def get_character(default=DEFAULT_CHARACTER, target='') -> dict:
    target = target if target != '' else CHARACTER
    try:
        chacs = jsontools.read_from_path(f"./XDS-bot-qq/characters/{target}.json")
    except:
        chacs = False
    result = chacs if chacs else False
    if target == DEFAULT_CHARACTER and not result:
        return {}
    return result if result else get_character(default=default, target=DEFAULT_CHARACTER)

def get_character_item(*keys: str, character: str="", search_dict: dict | None=None):
    """得到角色字典对应键的值，如果找不到对应角色的值会返回默认的，还找不到则返回 default 值

    Args:
        *keys (str): 指定的键，会从左到右查找，类似于 dict[key0][key1][key2]...
        character (str, optional): 指定的角色名. Defaults to "".
        default (str, optional): 找不到值时返回的默认值. Defaults to "[NULL]".
        search_dict (dict | None, optional): 用于搜索的字典. Defaults to None.

    Returns:
        Any: 字典键对应的值
    """
    if not search_dict:
        if not character:
            search_dict = get_character()
        else:
            search_dict = get_character(target=character)
    try:
        result = dicttools.get_value(*keys, search_dict=search_dict)
    except KeyError:
        if character != DEFAULT_CHARACTER and CHARACTER != DEFAULT_CHARACTER:
            item = get_character_item(*keys, character=DEFAULT_CHARACTER)
            return item
        result = f"[获取消息错误：无法获取键组为 {keys} 的消息，如用户使用出现该问题，请截图交给九镹（并暴打九镹（？））]"
    return result

def get_message(*keys: str, character: str="", **kwargs) -> str:
    """获取 bot 角色字典消息

    Args:
        *keys (str): 消息键
        default (str, optional): 找不到值时返回的默认值. Defaults to "[bot 未输出任何消息 请私信 bot 并发送相关聊天记录/图片报告问题 xwx (遇到这件事请截图并且暴打九九)]".
        character (str, optional): 指定的角色名. Defaults to "".
        **kwargs: 格式化参数

    Returns:
        str: 消息字符串
    """
    try:
        result = get_character_item(*keys, character=character)
    except:
        return f"[获取消息错误：无法获取键组为 {keys} 的消息，如用户使用出现该问题，请截图交给九镹（并暴打九镹（？））]"

    result = str_choice(result)
    # if len(kwargs) < 1:
    #     return str(result).format()
    # 格式化参数文本
    for k, v in kwargs.items():
        if type(v) == list:
            for i, item in enumerate(v):
                if type(item) == int:
                    v[i] = f"{item:,}"
        elif type(v) == int:
            v = f"{v:,}"
        kwargs[k] = v
    # feedbacks = get_character_item("bot_info", "feedbacks")
    # print(feedbacks)
    try:
        return str(result).format(
            **kwargs,
            bot_name=get_character_item("bot_info", "name"),
            cmd_sep=["!", "！"]
        )
    except KeyError as ex:
        print(f"keyerror: {ex}")
        return str(result)

