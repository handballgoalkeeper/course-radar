import os
from datetime import date

from scrapy.settings import Settings

from course_radar.log_handler.enums.log_levels import LogLevel


class LoggerBase:
    def __init__(self, config: Settings, name: str, default_log_level: LogLevel = LogLevel.INFO) -> None:
        self.name = name
        self.config = config
        self.LOG_FILE_PATH = os.path.join(self.config.get('LOG_FOLDER_PATH'),
                                          f"log-{date.today().strftime('%Y%m%d')}.log")
        self.default_log_level = default_log_level
        self.__setup_log_file()

    def __setup_log_file(self) -> None:
        if not self.__today_log_file_exists():
            is_folder_created = False

            if not self.__log_folder_exists():
                os.mkdir(self.config.get('LOG_FOLDER_PATH'))
                is_folder_created = True

            with open(self.LOG_FILE_PATH, "w", encoding="UTF-8"):
                pass

            if is_folder_created:
                self.write_to_file(f'Logs folder created at path "{os.path.normpath(self.config.get('LOG_FOLDER_PATH'))}".')

            self.write_to_file(f'Today\'s log file created at path "{os.path.normpath(self.LOG_FILE_PATH)}".')

    def __log_folder_exists(self) -> bool:
        print(self.config)
        folder_path = self.config.get('LOG_FOLDER_PATH')

        return os.path.exists(folder_path) and os.path.isdir(folder_path)

    def __today_log_file_exists(self) -> bool:
        return os.path.exists(self.LOG_FILE_PATH) and os.path.isfile(self.LOG_FILE_PATH)

    def write_to_file(self, message: str) -> None:
        self.__setup_log_file()
        with open(self.LOG_FILE_PATH, 'a', encoding="UTF-8") as today_log_file:
            today_log_file.write(f"{message}\n")