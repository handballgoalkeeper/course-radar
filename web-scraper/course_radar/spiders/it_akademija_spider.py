from dataclasses import asdict

import scrapy
from scrapy.http import Response
from scrapy.selector import SelectorList

from course_radar.dtos.course_dto import CourseDTO
from course_radar.dtos.course_provider_dto import CourseProviderDto
from course_radar.mappers.it_akademija.package_mapper import PackageMapper

from course_radar.wrappers.xpath_wrapper import XPathWrapper, XPathBuilder

class ItAkademijaSpiderSpider(scrapy.Spider):
    # -----DON'T DELETE THIS-----
    id = 1#                     |
    # ---------------------------
    course_provider = CourseProviderDto(spider_id= 1, name='IT Akademija', web_site_url='https://www.it-akademija.com')
    name = "it_akademija_spider"
    allowed_domains = ["www.it-akademija.com"]
    start_urls = ["https://www.it-akademija.com/birajte-sest-odseka-it-strucnost-zvanicna-zvanja-eksperata"]

    def parse(self, response, **kwargs):
        course_links = self.__get_courses_links(response)

        for course_name in list(course_links.keys()):
            course = CourseDTO()
            course.title = course_name
            course.description = ''

            yield response.follow(course_links[course_name], self.__parse_course_main, meta={
                'course': course
            })

    def __get_courses_names(self, response: Response) -> list:
        courses_names = (
            XPathWrapper(
                root_element=response,
                search_relative_to_root_element=True
            )
            .with_recursive(
                element=XPathBuilder.Element.ASIDE,
                constraints=[
                    XPathBuilder.Constraint(
                        constraint_part='normalize-space(@id) = "mainSidebar"'
                    )
                ]
            )
            .with_recursive(
                element=XPathBuilder.Element.NAV,
                constraints=[
                    XPathBuilder.Constraint(
                        constraint_part='normalize-space(@id) = "sidebarNav"'
                    )
                ]
            )
            .with_recursive(
                element=XPathBuilder.Element.DIV,
                constraints=[
                    XPathBuilder.Constraint(
                        constraint_part='normalize-space(@class) = "accord-content"'
                    )
                ]
            )
            .with_recursive(
                element=XPathBuilder.Element.A
            )
            .inner_text()
            .get_all()
        )

        return [name.strip() for name in courses_names if name.strip() != '']

    def __get_courses_links(self, response: Response) -> dict[str, str]:
        links = (
            XPathWrapper(
                root_element=response,
                search_relative_to_root_element=True
            )
            .with_recursive(
                element=XPathBuilder.Element.ASIDE,
                constraints=[
                    XPathBuilder.Constraint(
                        constraint_part='normalize-space(@id) = "mainSidebar"'
                    )
                ]
            )
            .with_recursive(
                element=XPathBuilder.Element.NAV,
                constraints=[
                    XPathBuilder.Constraint(
                        constraint_part='normalize-space(@id) = "sidebarNav"'
                    )
                ]
            )
            .with_recursive(
                element=XPathBuilder.Element.DIV,
                constraints=[
                    XPathBuilder.Constraint(
                        constraint_part='normalize-space(@class) = "accord-content"'
                    )
                ]
            )
            .with_recursive(
                element=XPathBuilder.Element.A
            )
            .get_attribute_content(
                attribute = XPathBuilder.Attribute.HREF
            )
            .get_all()
        )
        names = self.__get_courses_names(response)

        return dict(zip(names, links))

    def __parse_course_main(self, response: Response):
        course: CourseDTO = response.meta.get('course')

        if course.packages is None:
            course_link = response.url

            packages_link = 'https://www.it-akademija.com/upis-it-akademija-prijavite-se-na-vreme'
            yield response.follow(packages_link, self.__parse_packages_page, meta={
                'course': course,
                'course_link': course_link
            })
        else:
            # noinspection PyTypeChecker
            yield asdict(course)

    def __parse_packages_page(self, response: Response):
        course: CourseDTO = response.meta.get('course')
        course_link = response.meta.get('course_link')

        price_table = (
            XPathWrapper(
                root_element = response,
                search_relative_to_root_element = True
            )
            .with_recursive(
                element=XPathBuilder.Element.DIV,
                constraints=[
                    XPathBuilder.Constraint(
                        constraint_part='normalize-space(@id) = "wrapper"'
                    )
                ]
            )
            .with_recursive(
                element=XPathBuilder.Element.DIV,
                constraints=[
                    XPathBuilder.Constraint(
                        constraint_part='normalize-space(@id) = "content"'
                    )
                ]
            )
            .with_recursive(
                element=XPathBuilder.Element.TABLE,
                constraints=[
                    XPathBuilder.Constraint(
                        constraint_part='normalize-space(@class) = "tabela"'
                    )
                ]
            )
            .get_selector_list()
        )

        packages_table_rows = (
            XPathWrapper(
                root_element = price_table[-1],
                search_relative_to_root_element = True
            )
            .with_recursive(
                element=XPathBuilder.Element.TBODY,
            )
            .with_recursive(
                element=XPathBuilder.Element.TR
            )
            .get_selector_list()
        )[1:]

        packages = PackageMapper.parse_package_list(packages_table_rows)

        course.packages = packages

        # noinspection PyTypeChecker
        yield response.follow(course_link, self.__parse_course_main, meta={'course': course})