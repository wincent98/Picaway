
import logging

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
# 创建日志记录器
logger = logging.getLogger('picaway_logger')

# 创建控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 创建文件处理器
file_handler = logging.FileHandler('app.log',encoding='utf-8')
file_handler.setLevel(logging.INFO)

# 定义日志消息格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# 将处理器添加到日志记录器
logger.addHandler(console_handler)
logger.addHandler(file_handler)

def getLogger():
    return logger
