from course_radar.database.mysql import MySQLWrapper
from course_radar.dtos.course_dto import CourseDTO
from course_radar.log_handler import create_logger
from course_radar.log_handler.enums.log_levels import LogLevel
from course_radar.mappers.course_mapper import CourseMapper
from course_radar.repositories.course_repository import CourseRepository


class CourseService:
    def __init__(self, config, mysql_db: MySQLWrapper):
        self.config = config
        self.logger = create_logger(config=self.config, name='CourseService')
        self.mysql_db = mysql_db
        self.course_repository = CourseRepository(
            mysql_db=self.mysql_db,
            config=self.config
        )

    def course_already_exists(self, course_name: str) -> bool:
        course_providers = self.course_repository.find_all_by_title(course_title=course_name)

        return len(course_providers) > 0

    def create(self, course: dict) -> CourseDTO:
        course_dto = CourseMapper.dict_to_dto(course)
        self.logger.write_to_file(f"Course '{course_dto.title}' created successfully.", LogLevel.SUCCESS)
        return self.course_repository.create(course = course_dto)
