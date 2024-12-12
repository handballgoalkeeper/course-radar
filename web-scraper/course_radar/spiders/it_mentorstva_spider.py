import scrapy
from scrapy import Selector
from scrapy.http import Response
from scrapy.selector import SelectorList

from course_radar.mappers.it_mentorstva_mapper import ItMentorstvaMapper


class ItMentorstvaSpider(scrapy.Spider):
    name = "it_mentorstva_spider"
    allowed_domains = ["itmentorstva.com"]
    start_urls = ["https://itmentorstva.com/kursevi-programiranja/"]


    def parse(self, response, **kwargs):
        elements = response.xpath(
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
        for element in elements:
            title = element.xpath(".//h4["
                                  "contains(@class, 'elementor-image-box-title')"
                                  "]"
                                  "//a"
                                  "//text()").get()

            description = " ".join(element.xpath(".//p["
                              "contains(@class, 'elementor-image-box-description')"
                              "]"
                              "//text()").get().split("\n"))

            link = element.xpath(".//div["
                                 "contains(@class, 'elementor-widget-container')"
                                 "]"
                                 "//a["
                                 "contains(@class, 'elementor-button elementor-button-link elementor-size-sm')"
                                 "]/@href").get()

            if link == "https://itmentorstva.com/nodejs-checkout":
                self.logger.info(f"Found a link: {link}")
                yield response.follow(link, self.__parse_price_page, meta={'title': title, 'description': description, 'link': None})
            else:
                ...

    def __parse_price_page(self, response: Response) -> dict:
        if response.meta.get('link') is None:
            # Pitati tomu, da li da mu scrapeujem i ove nevidljive sekcije...
            packets = response.xpath(".//main"
                                     "//section[not(contains(@class, 'elementor-hidden-desktop elementor-hidden-tablet elementor-hidden-mobile'))]"
                                     "//div["
                                     "contains(@class, 'elementor-container') and "
                                     "contains(@class, 'elementor-column-gap-no')"
                                     "]"
                                     "//div[normalize-space(@class) = 'elementor-price-table']")
            # packets = response.xpath(".//main"
            #                          "//div["
            #                          "contains(@class, 'elementor-container') and "
            #                          "contains(@class, 'elementor-column-gap-no')"
            #                          "]"
            #                          "//div[normalize-space(@class) = 'elementor-price-table']")

            counter = 1
            for packet in ItMentorstvaMapper.parse_packet_list(packets):
                yield packet
                self.logger.info(f"Crawled packet {counter}: {packet}")
                counter += 1