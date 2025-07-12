from hoshino import Service
from hoshino.typing import MessageSegment
import os
import random
import logging

# 创建本插件的logger
logger = logging.getLogger(__name__)

sv = Service('戳一戳语音', help_='戳一戳发送随机语音和提示消息', enable_on_default=False)

# 获取插件所在目录的record文件夹
current_dir = os.path.dirname(os.path.abspath(__file__))
RECORD_DIR = os.path.join(current_dir, 'record')

# 确保目录存在
if not os.path.exists(RECORD_DIR):
    os.makedirs(RECORD_DIR)
    logger.warning(f"语音文件夹不存在，已自动创建: {RECORD_DIR}")
else:
    logger.info(f"使用语音文件夹: {RECORD_DIR}")

@sv.on_notice('notify.poke')
async def poke_event(session):
    try:
        event = session.event
        logger.info(f"收到戳一戳事件 - 发送者: {event.user_id}, 目标: {event.target_id}")

        # 直接从事件中获取self_id和目标ID
        bot_self_id = str(event.self_id)
        target_id = str(event.target_id)
        
        logger.info(f"机器人self_id: {bot_self_id}, 目标ID: {target_id}")

        # 检查是否被戳的是机器人自己
        if target_id != bot_self_id:
            logger.info(f"忽略非机器人目标ID: {target_id}")
            return

        # 发送文本消息
        await session.send("请不要戳xcw了>_<")
        
        # 检查语音文件（.m4a格式）
        voice_files = [f for f in os.listdir(RECORD_DIR) if f.lower().endswith('.m4a')]
        
        if not voice_files:
            logger.error(f"没有找到.m4a语音文件，请检查 {RECORD_DIR} 目录")
            return

        logger.info(f"找到 {len(voice_files)} 个.m4a语音文件")

        # 随机选择并发送语音
        selected_voice = random.choice(voice_files)
        voice_path = os.path.join(RECORD_DIR, selected_voice).replace('\\', '/')
        logger.info(f"准备发送语音: {selected_voice}")

        # 构造语音消息
        voice_msg = MessageSegment.record(f'file:///{voice_path}')
        await session.send(voice_msg)
        logger.info("语音消息已发送")

    except Exception as e:
        logger.error(f"处理戳一戳时出错: {str(e)}", exc_info=True)