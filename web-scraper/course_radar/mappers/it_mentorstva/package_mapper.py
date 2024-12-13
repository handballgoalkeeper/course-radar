from dataclasses import asdict

from scrapy import Selector
from scrapy.selector import SelectorList

from course_radar.dtos.it_mentorstva.package_dto import PackageDTO


class PackageMapper:
    @staticmethod
    def parse_packet(packet: Selector) -> PackageDTO:
        dto = PackageDTO()
        dto.name = PackageMapper.__get_package_name(packet)
        dto.description = PackageMapper.__get_package_description(packet)
        dto.original_price = PackageMapper.__get_package_original_price(packet)
        dto.discounted_price = PackageMapper.__get_package_discounted_price(packet)
        dto.discount = PackageMapper.__get_package_discount(packet)
        dto.package_includes = PackageMapper.__get_package_includes(packet)
        return dto

    @staticmethod
    def parse_packet_list(packet_list: SelectorList) -> list[PackageDTO]:
        # noinspection PyTypeChecker
        return [PackageMapper.parse_packet(packet) for packet in packet_list]

    @staticmethod
    def __get_package_name(packet: Selector) -> str:
        return (packet.xpath(".//div[normalize-space(@class) = 'elementor-price-table__header']"
                             "//h3[normalize-space(@class) = 'elementor-price-table__heading']"
                             "/text()")
                .get()
                .strip()
                .title())

    @staticmethod
    def __get_package_description(packet: Selector) -> str:
        return ""

    @staticmethod
    def __get_package_original_price(packet: Selector):
        original_price_field_exists = True if packet.xpath(".//div[normalize-space(@class) = 'elementor-price-table__price']"
                                              "//div[contains(@class, 'elementor-price-table__original-price') and contains(@class, 'elementor-typo-excluded')]"
                                              "/text()").get() is not None else False

        if original_price_field_exists:
            return float(''.join(packet.xpath(".//div[normalize-space(@class) = 'elementor-price-table__price']"
                                              "//div[contains(@class, 'elementor-price-table__original-price') and contains(@class, 'elementor-typo-excluded')]"
                                              "/text()").getall()).strip())

        return float(packet.xpath(".//div[normalize-space(@class) = 'elementor-price-table__price']"
                                              "//span[normalize-space(@class) = 'elementor-price-table__integer-part']"
                                              "/text()").get())

    @staticmethod
    def __get_package_discounted_price(packet: Selector) -> float:
        return float(packet.xpath(".//div[normalize-space(@class) = 'elementor-price-table__price']"
                                  "//span[normalize-space(@class) = 'elementor-price-table__integer-part']"
                                  "/text()").get())

    @staticmethod
    def __get_package_discount(packet: Selector) -> float:
        discounted_by = PackageMapper.__get_package_original_price(
            packet) - PackageMapper.__get_package_discounted_price(packet)
        return round(discounted_by * 100 / PackageMapper.__get_package_original_price(packet), 2)

    @staticmethod
    def __get_package_includes(packet: Selector) -> list[str]:
        elements = packet.xpath(".//ul[normalize-space(@class) = 'elementor-price-table__features-list']"
                                "//li"
                                "//div[normalize-space(@class) = 'elementor-price-table__feature-inner']"
                                "//span/text()").getall()

        return [element.strip(': ') for element in elements if element.strip(': '   ).strip() != '']