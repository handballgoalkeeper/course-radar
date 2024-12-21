import mysql.connector
from scrapy.exceptions import DropItem

from course_radar.dtos.course_provider_dto import CourseProviderDto
from course_radar.dtos.package_dto import PackageDTO
from course_radar.dtos.course_dto import CourseDTO
from course_radar.database.mysql import MySQLWrapper
from course_radar.log_handler.enums.log_levels import LogLevel
from course_radar.mappers.package_include_mapper import PackageIncludeMapper
from course_radar.mappers.package_mapper import PackageMapper
from course_radar.services.course_provider_service import CourseProviderService

from course_radar.log_handler import create_logger
from course_radar.services.course_service import CourseService
from course_radar.services.package_include_service import PackageIncludeService
from course_radar.services.package_service import PackageService


class MySQLPipeline:
    def __init__(self, config):
        self.config = config
        self.global_logger = create_logger(name='Global', config=self.config)
        self.mysql_instance = MySQLWrapper(
            mysql_host=self.config.get("MYSQL_HOST"),
            mysql_user=self.config.get("MYSQL_USER"),
            mysql_password=self.config.get("MYSQL_PASSWORD"),
            mysql_db=self.config.get("MYSQL_DB")
        )
        self.course_provider_service = CourseProviderService(
            config=self.config,
            mysql_db=self.mysql_instance
        )

        self.course_service = CourseService(
            config=self.config,
            mysql_db=self.mysql_instance
        )

        self.package_service = PackageService(
            config=self.config,
            mysql_db=self.mysql_instance
        )

        self.package_include_service = PackageIncludeService(
            config=self.config,
            mysql_db=self.mysql_instance
        )

        self.conn = None
        self.cursor = None

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        return cls(config=crawler.settings)

    def open_spider(self, spider):
        try:
            self.global_logger.write_to_file(f"Spider '{spider.name}' started successfully.", LogLevel.SUCCESS)
            self.mysql_instance.start_transaction()

            self.__create_or_update_course_provider(
                course_provider=spider.course_provider
            )
        except mysql.connector.Error or Exception as e:
            self.mysql_instance.rollback()
            raise DropItem(str(e))

    def close_spider(self, spider):
        try:
            if self.mysql_instance.conn:
                self.mysql_instance.conn.commit()
        except mysql.connector.Error as e:
            print(f"Error committing transaction: {e}")
            if self.mysql_instance.conn:
                self.mysql_instance.rollback()
            raise DropItem("Failed to commit transaction")
        finally:
            self.mysql_instance.destroy()

    def process_item(self, item, spider):
        try:
            course_provider = self.course_provider_service.find_one_by_name(course_provider_name=spider.course_provider.name)

            if not self.course_service.course_already_exists(item['title']):
                item['course_provider_id'] = course_provider.id
                new_course = self.course_service.create(item)

                packages = PackageMapper.list_of_dict_to_list_of_dto(item['packages'])

                for package in packages:
                    package.course_id = new_course.id
                    package = self.package_service.create(package = package)

                    for package_include in package.package_includes:
                        package_include_dict = {
                            'text': package_include,
                            'package_id': package.id
                        }

                        # TO THINK: Potentially move this into a single column in packages table...
                        package_include = PackageIncludeMapper.dict_to_dto(package_include_dict)
                        self.package_include_service.create(package_include = package_include)
            else:
                ...

        except mysql.connector.Error or Exception as e:
            print(f"Error executing query: {e}")
            if self.mysql_instance.conn:
                self.mysql_instance.rollback()
            raise DropItem("Failed to insert item into MySQL")

        return item

    def __create_or_update_course_provider(self, course_provider: CourseProviderDto):
        if not self.course_provider_service.course_provider_already_exists(spider_id=course_provider.spider_id):
            self.course_provider_service.create(course_provider=course_provider)
        else:
            self.course_provider_service.update(course_provider=course_provider)