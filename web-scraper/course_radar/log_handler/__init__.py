from scrapy.settings import Settings

from course_radar.log_handler.enums.log_file_types import LogFileType
from course_radar.log_handler.enums.log_levels import LogLevel
from course_radar.log_handler.log_file_logger import LogFileLogger
from course_radar.log_handler.logger_base import LoggerBase


def create_logger(config: Settings, name: str, log_file_type: LogFileType = LogFileType.LOG,
                  log_level: LogLevel = LogLevel.INFO) -> LoggerBase | LogFileLogger:
    from course_radar.log_handler.log_file_logger import LogFileLogger

    logger_types = {
        LogFileType.LOG: LogFileLogger
    }

    return logger_types[log_file_type](config, name, log_level)
