from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""
    # 发多少条消息算刷屏
    msg_count_threshold: int = 3
    # 平均每秒发多少消息算刷屏
    sec_avg_msgs: float | int = 0.8
    # 激活该功能的群组
    activated_groups: list[int] = [727949269]
    # 禁言时长（分钟）
    ban_mins: int = 2