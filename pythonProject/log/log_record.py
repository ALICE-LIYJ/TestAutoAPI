import logging
import os


def log_print():
    # 设置日志名称
    logger = logging.getLogger("signal_plus_api_log")
    # 如果已经实例过一个相同名字的 logger，则不用再追加 handler，避免重复日志
    if not logger.handlers:
        # 设置日志等级
        logger.setLevel(logging.INFO)
        # 设置打印格式
        formats = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
        # log文件路径
        filePath = os.path.dirname(os.path.dirname(__file__))
        file_url = logging.FileHandler(filePath + "/log/SignalPlus.log", mode="a+", encoding="utf8")
        # 赋予打印格式
        file_url.setFormatter(formats)
        logger.addHandler(file_url)
    return logger



if __name__ == '__main__':
    pass
