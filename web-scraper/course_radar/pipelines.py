import mysql.connector
from scrapy.exceptions import DropItem

from course_radar.dtos.package_dto import PackageDTO
from course_radar.dtos.course_dto import CourseDTO
from course_radar.dtos.course_provider_dto import CourseProviderDto

class MySQLPipeline:
    def __init__(self, mysql_host, mysql_db, mysql_user, mysql_password):
        self.mysql_host = mysql_host
        self.mysql_db = mysql_db
        self.mysql_user = mysql_user
        self.mysql_password = mysql_password
        self.conn = None
        self.cursor = None

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        mysql_host = crawler.settings.get('MYSQL_HOST')
        mysql_db = crawler.settings.get('MYSQL_DB')
        mysql_user = crawler.settings.get('MYSQL_USER')
        mysql_password = crawler.settings.get('MYSQL_PASSWORD')

        return cls(mysql_host, mysql_db, mysql_user, mysql_password)

    def open_spider(self, spider):
        try:
            self.conn = mysql.connector.connect(
                host=self.mysql_host,
                database=self.mysql_db,
                user=self.mysql_user,
                password=self.mysql_password
            )
            self.cursor = self.conn.cursor(dictionary=True)

            self.conn.start_transaction()

            self.__create_or_update_course_provider(
                course_provider=spider.course_provider,
                spider_id=spider.id
            )
        except mysql.connector.Error or Exception as e:
            self.conn.rollback()
            raise DropItem(str(e))

    def close_spider(self, spider):
        try:
            if self.conn:
                self.conn.commit()
        except mysql.connector.Error as e:
            print(f"Error committing transaction: {e}")
            if self.conn:
                self.conn.rollback()
            raise DropItem("Failed to commit transaction")
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()

    def process_item(self, item, spider):
        try:
            course_provider_id = self.__get_course_provider_id(course_provider=spider.course_provider)

            if not self.__course_already_exists(item):

                new_course_id = self.__create_course(
                    course_provider_id=course_provider_id,
                    item=item
                )

                self.__create_or_update_packages(
                    packages = item['packages'],
                    course_id = new_course_id
                )
            else:
                ...

        except mysql.connector.Error or Exception as e:
            print(f"Error executing query: {e}")
            if self.conn:
                self.conn.rollback()
            raise DropItem("Failed to insert item into MySQL")

        return item

    def __create_course_provider(self, course_provider, spider_id):
        self.cursor.execute("""
                            INSERT INTO {table_name} (
                                name,
                                web_site_url,
                                spider_id,
                                created_at,
                                updated_at
                            ) VALUES (
                                %s,
                                %s,
                                %s,
                                CURRENT_TIMESTAMP,
                                CURRENT_TIMESTAMP
                            )
                        """.format(table_name=course_provider.__table__),
                            (course_provider.name, course_provider.web_site_url, spider_id,))

    def __course_provider_exists(self, course_provider, spider_id) -> bool:
        self.cursor.execute("SELECT count(*) AS 'count' FROM {table_name} WHERE spider_id=%s"
                            .format(table_name=course_provider.__table__),
                            (spider_id,))

        return self.cursor.fetchone()['count'] > 0

    def __update_course_provider(self, course_provider, spider_id):
        self.cursor.execute("SELECT id, name, web_site_url FROM {table_name} WHERE spider_id=%s"
                            .format(table_name=course_provider.__table__),
                            (spider_id, ))

        current_state = self.cursor.fetchone()

        if current_state['name'] != course_provider.name:
            self.cursor.execute("UPDATE {table_name} SET name=%s, updated_at=CURRENT_TIMESTAMP WHERE id=%s"
                                .format(table_name=course_provider.__table__),
                                (course_provider.name, current_state['id'],))

        if current_state['web_site_url'] != course_provider.web_site_url:
            self.cursor.execute("UPDATE {table_name} SET web_site_url=%s, updated_at=CURRENT_TIMESTAMP WHERE id=%s"
                                .format(table_name=course_provider.__table__),
                                (course_provider.web_site_url, current_state['id'],))

    def __create_or_update_course_provider(self, course_provider, spider_id):
        if not self.__course_provider_exists(
                course_provider=course_provider,
                spider_id=spider_id
        ):
            self.__create_course_provider(
                course_provider=course_provider,
                spider_id=spider_id
            )
        else:
            self.__update_course_provider(
                course_provider=course_provider,
                spider_id=spider_id
            )

    def __get_course_provider_id(self, course_provider):
        self.cursor.execute("SELECT id FROM {table_name} WHERE name=%s"
                            .format(table_name=course_provider.__table__), (course_provider.name,))

        return self.cursor.fetchone()['id']

    def __course_already_exists(self, item) -> bool:
        self.cursor.execute("SELECT count(*) AS 'count' FROM {table_name} WHERE title = %s"
                            .format(table_name=CourseDTO.__table__), (item['title'],))

        return self.cursor.fetchone()['count'] > 0

    def __create_course(self, course_provider_id, item):
        self.cursor.execute("""
                            INSERT INTO {table_name} (
                                course_provider_id,
                                title,
                                description,
                                created_at,
                                updated_at
                            ) VALUES (
                                %s,
                                %s,
                                %s,
                                CURRENT_TIMESTAMP,
                                CURRENT_TIMESTAMP
                            )
                        """.format(table_name=CourseDTO.__table__),
                            (course_provider_id, item['title'], item['description'],))

        self.cursor.execute("SELECT id FROM {table_name} ORDER BY id DESC LIMIT 1"
                            .format(table_name=CourseDTO.__table__))

        return self.cursor.fetchone()['id']

    def __create_or_update_packages(self, packages, course_id):
        for package in packages:
           if not self.__package_already_exists(package, course_id):
               new_package_id = self.__create_package(
                   package = package,
                   course_id = course_id
               )
           else:
               package_id = self.__update_package(
                   package = package
               )

    def __package_already_exists(self, package, course_id):
        self.cursor.execute("SELECT count(*) AS 'count' FROM {table_name} WHERE course_id=%s AND name=%s"
                            .format(table_name=PackageDTO.__table__), (course_id, package['name'], ))

        return self.cursor.fetchone()['count'] > 0

    def __create_package(self, package, course_id):
        self.cursor.execute("""
            INSERT INTO {table_name} (
                course_id,
                name,
                description,
                original_price,
                discounted_price,
                created_at,
                updated_at
            ) VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                CURRENT_TIMESTAMP,
                CURRENT_TIMESTAMP
            )
        """.format(table_name=PackageDTO.__table__), (
            course_id,
            package['name'],
            package['description'],
            package['original_price'],
            package['discounted_price'],
        ))

        self.cursor.execute("SELECT id FROM {table_name} ORDER BY id DESC LIMIT 1"
                            .format(table_name=PackageDTO.__table__))

        return self.cursor.fetchone()['id']

    def __update_package(self, package):
        self.cursor.execute("SELECT id, name, description, original_price, discounted_price FROM {table_name} WHERE name=%s"
                            .format(table_name=PackageDTO.__table__), (package['name'], ))

        current_state = self.cursor.fetchone()

        if current_state['description'] != package['description']:
            self.cursor.execute("UPDATE {table_name} SET description=%s WHERE id=%s"
                                .format(table_name=PackageDTO.__table__),
                                (package['description'], current_state['id']))

        if current_state['original_price'] != package['original_price']:
            self.cursor.execute("UPDATE {table_name} SET original_price=%s WHERE id=%s"
                                .format(table_name=PackageDTO.__table__),
                                (package['original_price'], current_state['id']))

        if current_state['discounted_price'] != package['discounted_price']:
            self.cursor.execute("UPDATE {table_name} SET discounted_price=%s WHERE id=%s"
                                .format(table_name=PackageDTO.__table__),
                                (package['discounted_price'], current_state['id']))

        self.cursor.execute("UPDATE {table_name} SET updated_at=CURRENT_TIMESTAMP WHERE id=%s"
                            .format(table_name=PackageDTO.__table__),
                            (current_state['id'], ))

        return current_state['id']