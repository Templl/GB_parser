import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
import pprint

class SJSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ["https://www.superjob.ru/vacancy/search/?keywords=анализ%20данных&catalogues%5B0%5D=33&geo%5Bt%5D%5B0%5D=4&click_from=facet']"]

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(
            "//a[@class='_1IHWd _6Nb0L _37aW8 _2qMLS f-test-button-dalshe f-test-link-Dalshe']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath("//span[@class='_3y3l6 z4PWH _2Rwtu']//@href").getall()
        for link in links:

            yield response.follow(link, callback=self.parse_vacancy)

    def parse_vacancy(self, response: HtmlResponse):
        name = response.xpath("//h1/text()").get()
        salary = response.xpath("//span[@class='_2eYAG _3y3l6 z4PWH t0SHb']/text()").getall()
        # print(salary)
        url = response.url
        print()
        yield JobparserItem(name=name, salary=salary, url=url)