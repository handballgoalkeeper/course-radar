from dataclasses import asdict

import scrapy
from scrapy.http import Response

from course_radar.dtos.course_dto import CourseDTO
from course_radar.mappers.it_akademija.package_mapper import PackageMapper


class ItAkademijaSpiderSpider(scrapy.Spider):
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
        courses_names = response.xpath(".//aside[normalize-space(@id) = 'mainSidebar']"
                                       "//nav[normalize-space(@id) = 'sidebarNav']"
                                       "//div[normalize-space(@class) = 'accord-content']"
                                       "//a"
                                       "/text()").getall()

        return [name.strip() for name in courses_names if name.strip() != '']

    def __get_courses_links(self, response: Response) -> dict[str, str]:
        links = response.xpath(".//aside[normalize-space(@id) = 'mainSidebar']"
                                       "//nav[normalize-space(@id) = 'sidebarNav']"
                                       "//div[normalize-space(@class) = 'accord-content']"
                                       "//a"
                                       "/@href").getall()
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

        price_table = response.xpath(".//div[normalize-space(@id) = 'wrapper']"
                                     "//div[normalize-space(@id) = 'content']"
                                     "//table[normalize-space(@class) = 'tabela']")

        packages_table_rows = price_table[-1].xpath(".//tbody//tr")[1:]

        packages = PackageMapper.parse_package_list(packages_table_rows)

        course.packages = packages

        # noinspection PyTypeChecker
        yield response.follow(course_link, self.__parse_course_main, meta={'course': course})