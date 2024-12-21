import scrapy
from scrapy.http import Response
from dataclasses import asdict

from course_radar.dtos.course_dto import CourseDTO
from course_radar.mappers.it_mentorstva.course_mapper import CourseMapper
from course_radar.mappers.it_mentorstva.package_mapper import PackageMapper
from course_radar.dtos.course_provider_dto import CourseProviderDto

from course_radar.wrappers.xpath_wrapper import XPathWrapper, XPathBuilder

class ItMentorstvaSpider(scrapy.Spider):
    # -----DON'T DELETE THIS-----
    id = 2#                     |
    # ---------------------------
    course_provider = CourseProviderDto(spider_id=2, name='ITMentorstva', web_site_url='https://itmentorstva.com')
    name = "it_mentorstva_spider"
    allowed_domains = ["itmentorstva.com"]
    start_urls = ["https://itmentorstva.com/kursevi-programiranja/"]
    DIRECT_PRICE_PAGE_LINKS = [
        'https://itmentorstva.com/python-checkout',
        'https://itmentorstva.com/nodejs-checkout'
    ]

    def parse(self, response, **kwargs):
        courses_elements = (
            XPathWrapper(
                root_element = response
            )
            .with_recursive(
                element = XPathBuilder.Element.MAIN
            )
            .with_recursive(
                element = XPathBuilder.Element.SECTION
            )
            .with_recursive(
                element = XPathBuilder.Element.DIV,
                constraints = [
                    XPathBuilder.Constraint(
                        constraint_part = 'contains(@class, "elementor-container")'
                    ),
                    XPathBuilder.Constraint(
                        constraint_part = 'contains(@class, "elementor-column-gap-extended")'
                    )
                ]
            )
            .with_recursive(
                element = XPathBuilder.Element.DIV,
                constraints = [
                    XPathBuilder.Constraint(
                        constraint_part = 'contains(@class, "elementor-widget-wrap")'
                    ),
                    XPathBuilder.Constraint(
                        constraint_part = 'contains(@class, "elementor-element-populated")'
                    )
                ]
            )
            .get_selector_list()
        )

        # noinspection PyTypeChecker
        for element in courses_elements:
            course = CourseMapper.parse_course(element)

            next_link = CourseMapper.get_price_page_url(element)

            if next_link in ItMentorstvaSpider.DIRECT_PRICE_PAGE_LINKS:
                yield response.follow(next_link, self.__parse_price_page, meta={'course': course, 'link': None})
            else:
                yield response.follow(next_link, self.__parse_price_page, meta={'course': course, 'link': next_link})

    def __parse_price_page(self, response: Response) -> dict:
        course: CourseDTO = response.meta.get('course')

        if response.meta.get('link') is None:
            packets = response.xpath(
                XPathBuilder(start_relative_to_current_node = True)
                .with_recursive(
                    element = XPathBuilder.Element.SECTION,
                    constraints = [
                        XPathBuilder.Constraint(
                            constraint_part = 'not(contains(@class, "elementor-hidden-desktop elementor-hidden-tablet elementor-hidden-mobile"))'
                        )
                    ]
                )
                .with_recursive(
                    element = XPathBuilder.Element.DIV,
                    constraints = [
                        XPathBuilder.Constraint(
                            constraint_part = 'contains(@class, "elementor-container")'
                        ),
                        XPathBuilder.Constraint(
                            constraint_part = 'contains(@class, "elementor-column-gap-no")'
                        )
                    ]
                )
                .with_recursive(
                    element = XPathBuilder.Element.DIV,
                    constraints = [
                        XPathBuilder.Constraint(
                            constraint_part = 'normalize-space(@class) = "elementor-price-table"'
                        )
                    ]
                )
                .build()
            )

            # noinspection PyTypeChecker
            course.packages = PackageMapper.parse_packet_list(packets)
            # noinspection PyTypeChecker
            yield asdict(course)
        else:
            pricing_link = response.xpath(
                XPathBuilder(start_relative_to_current_node = True)
                .with_recursive(
                    element = XPathBuilder.Element.BODY
                )
                .with_recursive(
                    element = XPathBuilder.Element.A,
                    constraints = [
                        XPathBuilder.Constraint(
                            constraint_part = 'contains(@class, "elementor-button")'
                        ),
                        XPathBuilder.Constraint(
                            constraint_part = 'contains(@class, "elementor-button-link")'
                        ),
                        XPathBuilder.Constraint(
                            constraint_part = 'contains(@class, "elementor-size-sm")'
                        ),
                        XPathBuilder.Constraint(
                            constraint_part = 'contains(@class, "elementor-animation-float")'
                        )
                    ]
                )
                .get_attribute_content(
                    attribute = XPathBuilder.Attribute.HREF
                )
                .build()
            ).get()

            yield response.follow(pricing_link, self.__parse_price_page, meta={'course': course, 'link': None})