from course_radar.dtos.course_dto import CourseDTO


class CourseMapper:
    @staticmethod
    def dict_to_dto(data: dict) -> CourseDTO:
        dto = CourseDTO()
        dto.title = data['title']
        dto.description = data['description']

        if 'course_provider_id' in data:
            dto.course_provider_id = data['course_provider_id']

        return dto