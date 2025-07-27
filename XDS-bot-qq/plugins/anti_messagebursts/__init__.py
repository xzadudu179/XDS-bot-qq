from nonebot import get_driver, get_plugin_config
from nonebot import get_bot
from xmetools.bottools import check_group_stats
from nonebot import logger
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from xmetools.chactools import get_message
from xmetools.bottools import get_group_member_name, bot_isadmin
from nonebot.plugin import PluginMetadata, on_message
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
import time
# from xmetools import cmdtools

from .config import Config

last_messages = {
    "refresh_time": 0
}

__plugin_meta__ = PluginMetadata(
    name="anti_messagebursts",
    description="",
    usage="",
    config=Config,
)

global_config = get_driver().config

anti_messagebursts = on_message(priority=3, block=True)
@anti_messagebursts.handle()
@check_group_stats(config=get_plugin_config(__plugin_meta__.config), permissions=[bot_isadmin])
async def handle_message(event: GroupMessageEvent):
    config = get_plugin_config(__plugin_meta__.config)
    bot = get_bot()
    global last_messages
    # recalls = json_tools.read_from_path('./recalls.json')['recalls']
    MSG_COUNT_THRESHOLD = config.msg_count_threshold
    SEC_AVG_MSGS = config.sec_avg_msgs
    try:
        key = f"{event.user_id}{event.group_id}"
    except:
        anti_messagebursts.destroy()
    # if event['user_id'] == event.self_id:
    #     return
    message = x if (x:=event.raw_message.strip()) else event.raw_message
    # 不处理空消息了
    if not message:
        anti_messagebursts.destroy()
    if time.time() - last_messages['refresh_time'] > (SEC_AVG_MSGS * MSG_COUNT_THRESHOLD * 2) and last_messages['refresh_time'] > 0:
        # logger.info(last_messages)
        # logger.info(f"正在清除以上消息的缓存...")
        last_messages = {
            "refresh_time": time.time()
        }
    elif last_messages['refresh_time'] <= 0:
        last_messages['refresh_time'] = time.time()
    last_messages.setdefault(key, {}).setdefault(message, {})
    last_messages[key][message].setdefault("count", 0)
    if not last_messages[key][message].get("start_time", False):
        # logger.info(f"记录新语句: {message}")
        last_messages[key][message]["start_time"] = time.time()
    last_messages[key][message]['count'] += 1
    if not last_messages[key][message].get("banned", False):
        last_messages[key][message]["banned"] = False
    # logger.info(last_messages)

    if last_messages[key][message]['count'] >= MSG_COUNT_THRESHOLD:
        # 刷屏了 禁言
        if event.user_id == event.self_id:
            # 把自己刷屏的内容撤回
            await bot.delete_msg(message_id=event.message_id)
            logger.info(f"消息 \"{event.raw_message}\" 刷屏，不处理")
            anti_messagebursts.destroy()
        # 如果在 x 秒内发的消息超过这么多则算刷屏
        time_period = time.time() - last_messages[key][message]["start_time"]
        logger.info(f'{event.user_id} 在 {time_period:.2f} 秒发了 {last_messages[key][message]["count"]} 条消息 {message}，平均条消息间隔 {(time_period / last_messages[key][message]["count"]):.2f} 秒\n刷屏限制为一条间隔 {SEC_AVG_MSGS} 秒')
        if time_period > (SEC_AVG_MSGS * last_messages[key][message]['count']): return
        if last_messages[key][message]['count'] < MSG_COUNT_THRESHOLD * 4:
            last_messages['refresh_time'] = time.time()
        if not last_messages[key][message]["banned"]:
            # 禁言 / 提醒
            logger.info(f"消息 \"{message}\" 刷屏了")
            last_messages[key][message]["banned"] = True
            logger.info(f"尝试禁言群员")
            await bot.set_group_ban(group_id=event.group_id, user_id=event.user_id, duration=config.ban_mins * 60)
            logger.info("提醒群员")
            # await bot.send_group_msg(message=get_message("event_parsers", "cmd_bursts" if is_cmd else "message_bursts"), group_id=event.group_id)
            await anti_messagebursts.finish(message=get_message("plugins", __plugin_meta__.name, "message_bursts", mins=config.ban_mins, count=last_messages[key][message]['count'], secs=f"{time_period:2f}", user=await get_group_member_name(event)))
            # await bot.send_group_msg(message=get_message("event_parsers", "cmd_bursts" if is_cmd else "message_bursts"), group_id=event.group_id)
        logger.info(f"消息 \"{event.raw_message}\" 刷屏，不处理")
        anti_messagebursts.destroy()
    return