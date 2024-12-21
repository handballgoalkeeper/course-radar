from scrapy import Selector
from scrapy.http import Response
from scrapy.selector import SelectorList
from course_radar.builders.xpath_builder import XPathBuilder

class XPathWrapper:
    def __init__(self, root_element: Selector | Response | SelectorList, search_relative_to_root_element: bool = False) -> None:
        self.__path_builder = XPathBuilder(start_relative_to_current_node = search_relative_to_root_element)
        self.root_element = root_element

    def with_recursive(self, element: XPathBuilder.Element, constraints: list[XPathBuilder.Constraint] = None) -> 'XPathWrapper':
        self.__path_builder.with_recursive(element, constraints)
        return self

    def single_depth(self, element: XPathBuilder.Element) -> 'XPathWrapper':
        self.__path_builder.single_depth(element)
        return self

    def get(self)-> str | None:
        xpath_string = self.__path_builder.build()

        return self.root_element.xpath(xpath_string).get()

    def get_all(self) -> list[str]:
        xpath_string = self.__path_builder.build()
        return self.root_element.xpath(xpath_string).getall()

    def get_selector_list(self) -> SelectorList:
        xpath_string = self.__path_builder.build()
        return self.root_element.xpath(xpath_string)

    def inner_text(self, recursive: bool = False) -> 'XPathWrapper':
        self.__path_builder.inner_text(recursive = recursive)
        return self

    def get_attribute_content(self, attribute: 'XPathBuilder.Attribute' , recursive: bool = False) -> 'XPathWrapper':
        self.__path_builder.get_attribute_content(attribute, recursive = recursive)
        return self