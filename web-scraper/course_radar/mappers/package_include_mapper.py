from course_radar.dtos.package_include_dto import PackageIncludeDTO


class PackageIncludeMapper:
    @staticmethod
    def dict_to_dto(data: dict) -> PackageIncludeDTO:
        dto = PackageIncludeDTO()
        dto.package_id = data['package_id']
        dto.text = data['text']
        return dto

    @staticmethod
    def list_of_dict_to_list_of_dto(data_list: list[dict]) -> list[PackageIncludeDTO]:
        return [PackageIncludeMapper.dict_to_dto(data) for data in data_list]