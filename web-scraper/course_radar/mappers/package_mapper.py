from course_radar.dtos.package_dto import PackageDTO


class PackageMapper:
    @staticmethod
    def dict_to_dto(data: dict) -> PackageDTO:
        dto = PackageDTO()
        dto.name = data['name']
        dto.description = data['description']
        dto.original_price = data['original_price']
        dto.discounted_price = data['discounted_price']
        dto.discount = data['discount']
        dto.package_includes = data['package_includes']
        return dto

    @staticmethod
    def list_of_dict_to_list_of_dto(data_list: list[dict]) -> list[PackageDTO]:
        return [PackageMapper.dict_to_dto(data) for data in data_list]