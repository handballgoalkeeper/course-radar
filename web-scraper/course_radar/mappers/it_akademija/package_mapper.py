from scrapy import Selector
from scrapy.selector import SelectorList

from course_radar.dtos.package_dto import PackageDTO


class PackageMapper:
    @staticmethod
    def parse_package(package: Selector) -> PackageDTO:
        dto = PackageDTO()
        dto.name = PackageMapper.__get_package_name(package)
        dto.description = ""
        dto.original_price = PackageMapper.__get_original_price(package)
        dto.discounted_price = PackageMapper.__get_discounted_price(package)
        dto.discount = PackageMapper.__get_discount(package)
        dto.package_includes = []
        return dto

    @staticmethod
    def parse_package_list(package_list: SelectorList) -> list[PackageDTO]:
        # noinspection PyTypeChecker
        return [PackageMapper.parse_package(package) for package in package_list]

    @staticmethod
    def __get_package_name(package: Selector) -> str:
        return package.xpath("./td/text()").get().strip()

    @staticmethod
    def __get_original_price(package: Selector) -> float:
        td_elements = package.xpath(".//td[normalize-space(@class) = 'CrveniTxt']/span/text()").getall()[0]
        return float(td_elements)

    @staticmethod
    def __get_discounted_price(package: Selector) -> float:
        td_elements = package.xpath(".//td[normalize-space(@class) = 'ZeleniTxt']/text()").getall()[0]
        return float(td_elements)

    @staticmethod
    def __get_discount(package: Selector) -> float:
        discounted_by = PackageMapper.__get_original_price(package) - PackageMapper.__get_discounted_price(package)
        return round(discounted_by * 100 / PackageMapper.__get_original_price(package), 2)

