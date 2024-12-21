from course_radar.database.mysql import MySQLWrapper
from course_radar.dtos.course_provider_dto import CourseProviderDto


class CourseProviderRepository:
    def __init__(self, config, mysql_db: MySQLWrapper):
        self.table_name = CourseProviderDto.__table__
        self.config = config
        self.mysql_db = mysql_db

    def find_all_by_spider_id(self, spider_id: int) -> list[dict]:
        self.mysql_db.cursor.execute("SELECT * FROM {table_name} WHERE spider_id = %s"
                                       .format(table_name=self.table_name), (spider_id,))

        results = self.mysql_db.cursor.fetchall()
        return results

    def create(self, course_provider: CourseProviderDto) -> CourseProviderDto:
        self.mysql_db.cursor.execute(
            """INSERT INTO {table_name} (
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
            )"""
            .format(table_name=course_provider.__table__),
                (course_provider.name, course_provider.web_site_url, course_provider.spider_id,))

        if not self.mysql_db.transaction_started:
            self.mysql_db.conn.commit()

        return course_provider

    def update_by_spider_id(self, course_provider: CourseProviderDto) -> CourseProviderDto:
        self.mysql_db.cursor.execute(
            "UPDATE {table_name}"
            " SET name = %s, web_site_url = %s, updated_at = CURRENT_TIMESTAMP"
            " WHERE spider_id = %s"
            .format(table_name=self.table_name),
            (course_provider.name, course_provider.web_site_url, course_provider.spider_id,))

        if not self.mysql_db.transaction_started:
            self.mysql_db.conn.commit()

        return course_provider

    def find_one_by_name(self, course_provider_name: str) -> dict:
        self.mysql_db.cursor.execute("SELECT id, name, web_site_url, spider_id FROM {table_name}"
                                     " WHERE name = %s".format(table_name=self.table_name), (course_provider_name,))

        results = self.mysql_db.cursor.fetchone()

        if results is None:
            raise Exception("Course provider name not found")

        return results