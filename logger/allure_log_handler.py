import allure
from loguru import logger

class AllureLogHandler:
    def write(self, message):
        allure.attach(message, attachment_type=allure.attachment_type.TEXT)

# 创建Loguru日志处理程序实例
log_handler = AllureLogHandler()
# 将Loguru日志处理程序添加到Loguru日志记录器
logger.add(log_handler)