from scrapy import Selector
from scrapy.selector import SelectorList
from course_radar.wrappers.xpath_wrapper import XPathWrapper, XPathBuilder

from course_radar.dtos.course_dto import CourseDTO


class CourseMapper:
    @staticmethod
    def __get_title(element: Selector) -> str:
        return (
            XPathWrapper(
                root_element = element,
                search_relative_to_root_element = True
            )
            .with_recursive(
                element = XPathBuilder.Element.H4,
                constraints = [
                    XPathBuilder.Constraint(
                        constraint_part = 'contains(@class, "elementor-image-box-title")'
                    )
                ]
            )
            .with_recursive(element=XPathBuilder.Element.A)
            .inner_text()
            .get()
        )

    @staticmethod
    def __get_description(element: Selector) -> str:
        return " ".join(
            XPathWrapper(
                root_element = element,
                search_relative_to_root_element = True
            )
            .with_recursive(
                element = XPathBuilder.Element.P,
                constraints = [
                    XPathBuilder.Constraint(
                        constraint_part = 'contains(@class, "elementor-image-box-description")'
                    )
                ]
            )
            .inner_text(recursive=True)
            .get()
            .split("\n")
        )

    @staticmethod
    def get_price_page_url(element: Selector) -> str:
        return (
            XPathWrapper(
                root_element = element,
                search_relative_to_root_element = True
            )
            .with_recursive(
                element = XPathBuilder.Element.DIV,
                constraints = [
                    XPathBuilder.Constraint(
                        constraint_part = 'contains(@class, "elementor-widget-container")'
                    )
                ]
            )
            .with_recursive(
                element = XPathBuilder.Element.A,
                constraints = [
                    XPathBuilder.Constraint(
                        constraint_part = 'contains(@class, "elementor-button elementor-button-link elementor-size-sm")'
                    )
                ]
            )
            .get_attribute_content(
                attribute = XPathBuilder.Attribute.HREF
            )
            .get()
        )

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