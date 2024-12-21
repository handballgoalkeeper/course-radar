from dataclasses import dataclass

from course_radar.dtos.package_dto import PackageDTO


@dataclass
class CourseDTO:
    __table__ = 'courses'
    title: str = None
    description: str = None
    packages: list[PackageDTO] = None
    course_provider_id: int = None
    id: int = None