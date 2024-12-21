from course_radar.database.mysql import MySQLWrapper
from course_radar.dtos.course_dto import CourseDTO


class CourseRepository:
    def __init__(self, config, mysql_db: MySQLWrapper):
        self.table_name = CourseDTO.__table__
        self.config = config
        self.mysql_db = mysql_db

    def find_all_by_title(self, course_title: str) -> list[dict]:
        self.mysql_db.cursor.execute("SELECT * FROM {table_name} WHERE title = %s"
                                     .format(table_name=self.table_name), (course_title,))

        results = self.mysql_db.cursor.fetchall()
        return results

    def create(self, course: CourseDTO) -> CourseDTO:
        self.mysql_db.cursor.execute(
            """INSERT INTO {table_name} (
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
            """.format(table_name=self.table_name),
            (course.course_provider_id, course.title, course.description, )
        )

        if not self.mysql_db.transaction_started:
            self.mysql_db.commit()

        self.mysql_db.cursor.execute("SELECT id FROM {table_name}"
                                     " WHERE title = %s".format(table_name=self.table_name), (course.title,))

        result = self.mysql_db.cursor.fetchone()

        if result is not None:
            course.id = result['id']

            return course

        raise Exception("Something went wrong.")