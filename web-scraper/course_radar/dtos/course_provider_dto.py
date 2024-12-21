from dataclasses import dataclass

@dataclass
class CourseProviderDto:
    __table__ = "course_providers"
    name: str
    web_site_url: str
    spider_id: int = None
    id: int = None
