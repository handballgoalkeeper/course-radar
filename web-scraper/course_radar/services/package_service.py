from course_radar.database.mysql import MySQLWrapper
from course_radar.dtos.package_dto import PackageDTO
from course_radar.log_handler import create_logger
from course_radar.log_handler.enums.log_levels import LogLevel
from course_radar.repositories.package_repository import PackageRepository


class PackageService:
    def __init__(self, config, mysql_db: MySQLWrapper):
        self.config = config
        self.logger = create_logger(config=self.config, name='CourseService')
        self.mysql_db = mysql_db
        self.package_repository = PackageRepository(
            mysql_db=self.mysql_db,
            config=self.config
        )

    def create(self, package: PackageDTO) -> PackageDTO:
        self.logger.write_to_file(f"Course '{package.name}' created successfully.", LogLevel.SUCCESS)
        return self.package_repository.create(package = package)