import scrapy
from scrapy.http import Response
from dataclasses import asdict

from course_radar.dtos.course_dto import CourseDTO
from course_radar.mappers.it_mentorstva.course_mapper import CourseMapper
from course_radar.mappers.it_mentorstva.package_mapper import PackageMapper


class ItMentorstvaSpider(scrapy.Spider):
    name = "it_mentorstva_spider"
    allowed_domains = ["itmentorstva.com"]
    start_urls = ["https://itmentorstva.com/kursevi-programiranja/"]
    DIRECT_PRICE_PAGE_LINKS = [
        'https://itmentorstva.com/python-checkout',
        'https://itmentorstva.com/nodejs-checkout'
    ]


    def parse(self, response, **kwargs):
        courses_elements = response.xpath(
            '//main'
            '//section'
            '//div['
            'contains(@class, "elementor-container") and '
            'contains(@class, "elementor-column-gap-extended")'
            ']'
            '//div['
            'contains(@class, "elementor-widget-wrap") and '
            'contains(@class, "elementor-element-populated")'
            ']'
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
            # packets = response.xpath(".//main"
            #                          "//section[not(contains(@class, 'elementor-hidden-desktop elementor-hidden-tablet elementor-hidden-mobile'))]"
            #                          "//div["
            #                          "contains(@class, 'elementor-container') and "
            #                          "contains(@class, 'elementor-column-gap-no')"
            #                          "]"
            #                          "//div[normalize-space(@class) = 'elementor-price-table']")
            packets = response.xpath(".//section[not(contains(@class, 'elementor-hidden-desktop elementor-hidden-tablet elementor-hidden-mobile'))]"
                                     "//div["
                                     "contains(@class, 'elementor-container') and "
                                     "contains(@class, 'elementor-column-gap-no')"
                                     "]"
                                     "//div[normalize-space(@class) = 'elementor-price-table']")

            # noinspection PyTypeChecker
            course.packages = PackageMapper.parse_packet_list(packets)
            # noinspection PyTypeChecker
            yield asdict(course)
        else:
            pricing_link = response.xpath(".//body//a["
                                          "contains(@class, 'elementor-button') and "
                                          "contains(@class, 'elementor-button-link') and "
                                          "contains(@class, 'elementor-size-sm') and "
                                          "contains(@class, 'elementor-animation-float')"
                                          "]"
                                          "/@href").get()

            yield response.follow(pricing_link, self.__parse_price_page, meta={'course': course, 'link': None})