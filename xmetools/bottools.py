from nonebot import get_bot
from nonebot.log import logger
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.permission import Permission
from xmetools.chactools import get_message
from functools import wraps

async def get_group_member_name(event: GroupMessageEvent):
    bot = get_bot()
    member = (await bot.get_group_member_info(group_id=event.group_id, user_id=event.user_id))
    card = member["card"]
    nickname = member["nickname"]
    return nickname if card is None else card

async def get_group_member_name_without_event(group_id, user_id):
    bot = get_bot()
    member = (await bot.get_group_member_info(group_id=group_id, user_id=user_id))
    card = member["card"]
    nickname = member["nickname"]
    return nickname if card is None else card

def check_group_stats(config, self_permissions: tuple, silent: bool = False):
    """检查是否在群组中插件的状态，包括激活，权限等

    Args:
        config (Config): 插件 Config，用于查看群组
        self_permissions (tuple): bot 自己所需的权限
        silent (bool, optional): 是否使控制台不输出. Defaults to False.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(event: GroupMessageEvent, *args, **kwargs):
            bot = get_bot()
            # perm = Permission(*self_permissions)
            # if not await perm(bot, event):
                # if not silent:
                    # logger.info(f"忽略执行，因为 bot 不符合 Permissions 条件 {self_permissions}")
            if event.group_id not in config.activated_groups:
                if not silent:
                    logger.info(f"忽略执行，因为 {event.group_id} 不在激活的群列表中。")
                return None
            return await func(event, *args, **kwargs)
        return wrapper
    return decorator