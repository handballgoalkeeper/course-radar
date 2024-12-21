from datetime import datetime

from scrapy.settings import Settings

from course_radar.log_handler.enums.log_levels import LogLevel
from course_radar.log_handler.logger_base import LoggerBase


class LogFileLogger(LoggerBase):
    def __init__(self, config: Settings, name: str, default_log_level) -> None:
        super().__init__(config, name, default_log_level)

    def write_to_file(self, message: str, log_level: LogLevel = None) -> None:
        if not log_level:
            log_level = self.default_log_level

        super().write_to_file(
            f"{datetime
               .now()
               .strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]} "
            f"[{log_level.value}] "
            f"[{self.name.capitalize()}] "
            f"{message}"
        )
