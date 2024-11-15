import logging

logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)  # 设置捕获所有大于等于DEBUG级别的消息

# 创建handler用于写入log文件
fh = logging.FileHandler('app.log')
fh.setLevel(logging.DEBUG)

# 创建formatter并添加到handler上
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

# 添加handler至logger对象
logger.addHandler(fh)


def get_logger() -> logging.Logger:
    return logger
