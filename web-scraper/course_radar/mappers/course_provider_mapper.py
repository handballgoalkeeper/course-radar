from course_radar.dtos.course_provider_dto import CourseProviderDto


class CourseProviderMapper:
    @staticmethod
    def dict_to_dto(data: dict) -> CourseProviderDto:
        dto = CourseProviderDto(
            name=data['name'],
            web_site_url=data['web_site_url']
        )

        if "spider_id" in data:
            dto.spider_id = data['spider_id']

        if 'id' in data:
            dto.id = data['id']

        return dto