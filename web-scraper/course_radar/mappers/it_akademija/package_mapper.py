from scrapy import Selector
from scrapy.selector import SelectorList

from course_radar.dtos.package_dto import PackageDTO
from course_radar.wrappers.xpath_wrapper import XPathWrapper, XPathBuilder


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
        return (
            XPathWrapper(
                root_element = package,
                search_relative_to_root_element=True
            )
            .single_depth(
                element=XPathBuilder.Element.TD
            )
            .inner_text()
            .get()
            .strip()
        )

    @staticmethod
    def __get_original_price(package: Selector) -> float:
        return float(
            XPathWrapper(
                root_element = package,
                search_relative_to_root_element = True
            )
            .with_recursive(
                element = XPathBuilder.Element.TD,
                constraints = [
                    XPathBuilder.Constraint(
                        constraint_part = 'normalize-space(@class) = "CrveniTxt"'
                    )
                ]
            )
            .single_depth(
                element = XPathBuilder.Element.SPAN
            )
            .inner_text()
            .get_all()[0]
        )

    @staticmethod
    def __get_discounted_price(package: Selector) -> float:
        return float(
            XPathWrapper(
                root_element = package,
                search_relative_to_root_element = True
            )
            .with_recursive(
                element = XPathBuilder.Element.TD,
                constraints = [
                    XPathBuilder.Constraint(
                        constraint_part = 'normalize-space(@class) = "ZeleniTxt"'
                    )
                ]
            )
            .inner_text()
            .get_all()[0]
        )

    @staticmethod
    def __get_discount(package: Selector) -> float:
        discounted_by = PackageMapper.__get_original_price(package) - PackageMapper.__get_discounted_price(package)
        return round(discounted_by * 100 / PackageMapper.__get_original_price(package), 2)

