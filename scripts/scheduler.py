"""
每日定时问候工作流 - Python调度器版本

运行方式：
    python scheduler.py

停止方式：
    Ctrl+C
"""

from apscheduler.schedulers.blocking import BlockingScheduler
from src.graphs.graph import main_graph
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建调度器
scheduler = BlockingScheduler()


# 7:30 - 发送天气预报
@scheduler.scheduled_job('cron', hour=7, minute=30)
def send_weather():
    """7:30 发送天气预报"""
    try:
        logger.info("开始发送天气预报...")
        result = main_graph.invoke({
            "city": "上海",
            "trigger_type": "weather"
        })
        logger.info(f"天气预报发送成功: {result.get('send_status')}")
    except Exception as e:
        logger.error(f"天气预报发送失败: {str(e)}")


# 7:31 - 发送早安问候（延迟1分钟，避免并发）
@scheduler.scheduled_job('cron', hour=7, minute=31)
def send_morning():
    """7:31 发送早安问候"""
    try:
        logger.info("开始发送早安问候...")
        result = main_graph.invoke({
            "city": "上海",
            "trigger_type": "morning"
        })
        logger.info(f"早安问候发送成功: {result.get('send_status')}")
    except Exception as e:
        logger.error(f"早安问候发送失败: {str(e)}")


# 22:30 - 发送晚安问候
@scheduler.scheduled_job('cron', hour=22, minute=30)
def send_evening():
    """22:30 发送晚安问候"""
    try:
        logger.info("开始发送晚安问候...")
        result = main_graph.invoke({
            "city": "上海",
            "trigger_type": "evening"
        })
        logger.info(f"晚安问候发送成功: {result.get('send_status')}")
    except Exception as e:
        logger.error(f"晚安问候发送失败: {str(e)}")


if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("每日定时问候工作流 - 已启动")
    logger.info("定时任务:")
    logger.info("  - 7:30  天气预报")
    logger.info("  - 7:31  早安问候")
    logger.info("  - 22:30 晚安问候")
    logger.info("按 Ctrl+C 停止")
    logger.info("=" * 50)

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("调度器已停止")
