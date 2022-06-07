import scrapy
from scrapy.http import HtmlResponse
from castoramaparser.items import CastoramaItem


class CastoramaruSpider(scrapy.Spider):
    name = 'castoramaru'
    allowed_domains = ['castorama.ru']
    start_urls = ['https://www.castorama.ru/tile/granite']

    def parse(self, response):
        links = response.xpath("//a[@class='product-card__img-link']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        name = response.xpath("//h1[@class = 'product-essential__name hide-max-small']/text()").get()
        # цена за упаковкку
        price = response.xpath("//span[@class='price']/span/span/text()").getall()[4]
        url = response.url
        photos = response.xpath("//ul[@class='swiper-wrapper']/li/img/@src").getall()
        yield CastoramaItem(name=name, price=price, url=url, photos=photos)


