import logging
from pathlib import Path


def get_logger(name: str):
    """
    创建并返回一个 logger。
    日志会同时输出到终端和 logs/agent.log。
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # 防止重复添加 handler
    if logger.handlers:
        return logger

    # 创建 logs 目录
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # 日志格式
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # 1. 终端输出
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # 2. 文件输出
    file_handler = logging.FileHandler(
        log_dir / "agent.log",
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    # 把两个输出渠道都交给 logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger