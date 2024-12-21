from course_radar.database.mysql import MySQLWrapper
from course_radar.dtos.course_provider_dto import CourseProviderDto
from course_radar.log_handler import create_logger
from course_radar.log_handler.enums.log_levels import LogLevel
from course_radar.mappers.course_provider_mapper import CourseProviderMapper
from course_radar.repositories.course_provider_repository import CourseProviderRepository

class CourseProviderService:
    def __init__(self, config, mysql_db: MySQLWrapper):
        self.config = config
        self.logger = create_logger(config=self.config, name='CourseProviderService')
        self.mysql_db = mysql_db
        self.course_provider_repository = CourseProviderRepository(
            mysql_db=self.mysql_db,
            config=self.config
        )

    def course_provider_already_exists(self, spider_id: int) -> bool:
        course_providers = self.course_provider_repository.find_all_by_spider_id(spider_id=spider_id)

        return len(course_providers) > 0

    def create(self, course_provider: CourseProviderDto) -> CourseProviderDto:
        course_provider = self.course_provider_repository.create(course_provider=course_provider)
        self.logger.write_to_file(f"Course provider {course_provider.name} created successfully.", LogLevel.INFO)
        return course_provider

    def update(self, course_provider: CourseProviderDto) -> CourseProviderDto:
        course_provider = self.course_provider_repository.update_by_spider_id(course_provider=course_provider)
        self.logger.write_to_file(f"Course provider update successfully.", LogLevel.INFO)
        return course_provider

    def find_one_by_name(self, course_provider_name: str) -> CourseProviderDto:
        return CourseProviderMapper.dict_to_dto(self.course_provider_repository.find_one_by_name(course_provider_name=course_provider_name))