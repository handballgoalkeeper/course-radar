from dataclasses import dataclass

from course_radar.dtos.package_dto import PackageDTO


@dataclass
class CourseDTO:
    title: str = None
    description: str = None
    packages: list[PackageDTO] = None