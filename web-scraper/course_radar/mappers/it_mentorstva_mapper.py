from scrapy import Selector
from scrapy.selector import SelectorList

from course_radar.dtos.it_mentorstva.package_dto import PackageDTO


class ItMentorstvaMapper:
    @staticmethod
    def parse_packet(packet: Selector)-> PackageDTO:
        dto = PackageDTO()
        dto.name = ItMentorstvaMapper.__get_package_name(packet)
        dto.description = ItMentorstvaMapper.__get_package_description(packet)
        dto.original_price = ItMentorstvaMapper.__get_package_original_price(packet)
        dto.discounted_price = ItMentorstvaMapper.__get_package_discounted_price(packet)
        dto.discount = ItMentorstvaMapper.__get_package_discount(packet)
        dto.package_includes = ItMentorstvaMapper.__get_package_includes(packet)
        return dto

    @staticmethod
    def parse_packet_list(packet_list: SelectorList)-> list[PackageDTO]:
        # noinspection PyTypeChecker
        return [ItMentorstvaMapper.parse_packet(packet) for packet in packet_list]

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
        return "test opis"

    @staticmethod
    def __get_package_original_price(packet: Selector) -> float:
        return 10

    @staticmethod
    def __get_package_discounted_price(packet: Selector) -> float:
        return 9

    @staticmethod
    def __get_package_discount(packet: Selector) -> float:
        discounted_by = ItMentorstvaMapper.__get_package_original_price(packet) - ItMentorstvaMapper.__get_package_discounted_price(packet)
        return discounted_by * 100 / ItMentorstvaMapper.__get_package_original_price(packet)

    @staticmethod
    def __get_package_includes(packet: Selector)-> list[str]:
        return ['Test include']