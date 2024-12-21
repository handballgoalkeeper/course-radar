from course_radar.database.mysql import MySQLWrapper
from course_radar.dtos.package_include_dto import PackageIncludeDTO


class PackageIncludeRepository:
    def __init__(self, config, mysql_db: MySQLWrapper):
        self.table_name = PackageIncludeDTO.__table__
        self.config = config
        self.mysql_db = mysql_db

    def create(self, package_include: PackageIncludeDTO) -> PackageIncludeDTO:
        self.mysql_db.cursor.execute(
            """INSERT INTO {table_name} (
                package_id,
                text,
                created_at
            ) VALUES (
                %s,
                %s,
                CURRENT_TIMESTAMP
            )
            """.format(table_name=self.table_name),
            (package_include.package_id, package_include.text, )
        )

        if not self.mysql_db.transaction_started:
            self.mysql_db.commit()

        self.mysql_db.cursor.execute("SELECT id FROM {table_name}"
                                     " WHERE text = %s AND package_id = %s"
                                     .format(table_name=self.table_name), (package_include.text, package_include.package_id)
        )

        result = self.mysql_db.cursor.fetchone()

        if result is not None:
            package_include.id = result['id']

            return package_include

        raise Exception("Something went wrong.")