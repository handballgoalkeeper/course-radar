from course_radar.database.mysql import MySQLWrapper
from course_radar.dtos.package_include_dto import PackageIncludeDTO
from course_radar.log_handler import create_logger
from course_radar.log_handler.enums.log_levels import LogLevel
from course_radar.repositories.package_include_repository import PackageIncludeRepository


class PackageIncludeService:
    def __init__(self, config, mysql_db: MySQLWrapper):
        self.config = config
        self.logger = create_logger(config=self.config, name='PackageIncludeService')
        self.mysql_db = mysql_db
        self.package_include_repository = PackageIncludeRepository(
            mysql_db=self.mysql_db,
            config=self.config
        )

    def create(self, package_include: PackageIncludeDTO) -> PackageIncludeDTO:
        package_include = self.package_include_repository.create(package_include=package_include)
        self.logger.write_to_file(f"Course '{package_include.text}' created successfully.", LogLevel.SUCCESS)
        return package_include
