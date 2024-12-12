from scrapy import Selector
from scrapy.selector import SelectorList


class ItMentorstvaMapper:
    @staticmethod
    def parse_packet(packet: Selector)-> dict:
        return {
            'name': ItMentorstvaMapper.__get_course_name(packet)
        }

    @staticmethod
    def parse_packet_list(packet_list: SelectorList)-> list[dict]:
        # noinspection PyTypeChecker
        return [ItMentorstvaMapper.parse_packet(packet) for packet in packet_list]

    @staticmethod
    def __get_course_name(packet: Selector) -> str:
        return (packet.xpath(".//div[normalize-space(@class) = 'elementor-price-table__header']"
                             "//h3[normalize-space(@class) = 'elementor-price-table__heading']"
                             "/text()")
                .get()
                .strip()
                .title())