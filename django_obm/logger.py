import logging

logging.addLevelName(logging.DEBUG, "🐛 DEBUG")
logging.addLevelName(logging.INFO, "📑 INFO")
logging.addLevelName(logging.WARNING, "⚠️ WARNING")
logging.addLevelName(logging.ERROR, "🚨 ERROR")
logging.addLevelName(logging.CRITICAL, "💥 CRITICAL")


def info_filter(record):
    return record.levelno < logging.WARNING


def get(name):
    logger = logging.getLogger(name)
    return logger
