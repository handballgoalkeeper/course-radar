from scrapy import Selector
from scrapy.selector import SelectorList

from course_radar.dtos.it_mentorstva.course_dto import CourseDTO


class CourseMapper:
    @staticmethod
    def __get_title(element: Selector) -> str:
        return element.xpath(".//h4["
                                  "contains(@class, 'elementor-image-box-title')"
                                  "]"
                                  "//a"
                                  "//text()").get()

    @staticmethod
    def __get_description(element: Selector) -> str:
        return " ".join(element.xpath(".//p["
                              "contains(@class, 'elementor-image-box-description')"
                              "]"
                              "//text()").get().split("\n"))

    @staticmethod
    def get_price_page_url(element: Selector) -> str:
        return element.xpath(".//div["
                                 "contains(@class, 'elementor-widget-container')"
                                 "]"
                                 "//a["
                                 "contains(@class, 'elementor-button elementor-button-link elementor-size-sm')"
                                 "]/@href").get()

    @staticmethod
    def parse_course(element: Selector) -> CourseDTO:
        dto = CourseDTO()
        dto.title = CourseMapper.__get_title(element)
        dto.description = CourseMapper.__get_description(element)
        return dto

    @staticmethod
    def parse_curse_list(element_list: SelectorList) -> list[CourseDTO]:
        # noinspection PyTypeChecker
        return [CourseMapper.parse_course(element) for element in element_list]