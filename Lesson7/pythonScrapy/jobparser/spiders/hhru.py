import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem



class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=анализ%20данных&catalogues%5B0%5D=33&geo%5Bt%5D%5B0%5D=4&click_from=facet']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@data-qa='pager-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[@data-qa="vacancy-serp__vacancy-title"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_vacancy)


    def parse_vacancy(self, response: HtmlResponse):
        name = response.css("h1::text").get()
        #name = response.xpath("//h1").get()
        salary = response.xpath('//div[@data-qa="vacancy-salary"]//text()').getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)



