from course_radar.database.mysql import MySQLWrapper
from course_radar.dtos.package_dto import PackageDTO


class PackageRepository:
    def __init__(self, config, mysql_db: MySQLWrapper):
        self.table_name = PackageDTO.__table__
        self.config = config
        self.mysql_db = mysql_db

    def create(self, package: PackageDTO) -> PackageDTO:
        self.mysql_db.cursor.execute(
            """INSERT INTO {table_name} (
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
            )""".format(table_name=self.table_name),
            (
                package.course_id,
                package.name,
                package.description,
                package.original_price,
                package.discounted_price
            )
        )

        if not self.mysql_db.transaction_started:
            self.mysql_db.commit()

        self.mysql_db.cursor.execute("SELECT id FROM {table_name}"
                                     " WHERE name = %s AND course_id = %s"
                                     .format(table_name=self.table_name),
                                     (package.name, package.course_id)
        )

        result = self.mysql_db.cursor.fetchone()

        if result is not None:
            package.id = result['id']

            return package

        raise Exception("Something went wrong.")