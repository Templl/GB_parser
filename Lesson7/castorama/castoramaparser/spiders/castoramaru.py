import scrapy
from scrapy.http import HtmlResponse
from castoramaparser.items import CastoramaItem
from scrapy.loader import ItemLoader


class CastoramaruSpider(scrapy.Spider):
    name = 'castoramaru'
    allowed_domains = ['castorama.ru']
    start_urls = ['https://www.castorama.ru/tile/granite']

    def parse(self, response):
        links = response.xpath("//a[@class='product-card__img-link']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=CastoramaItem(), response=response)
        loader.add_xpath('name', "//h1[@class = 'product-essential__name hide-max-small']/text()")
        loader.add_xpath('price', "//span[@class='price']/span/span/text()")
        loader.add_xpath('photos', "//li[contains(@class, 'top-slide swiper-slide')]/div/img/@data-src")
        loader.add_value('url', response.url)
        yield loader.load_item()

        #name = response.xpath("//h1[@class = 'product-essential__name hide-max-small']/text()").get()
        # цена за упаковкку
        #price = response.xpath("//span[@class='price']/span/span/text()").getall()[4]
        #url = response.url
        #photos = response.xpath("//li[contains(@class, 'top-slide swiper-slide')]/div/img/@data-src").getall()
        #yield CastoramaItem(name=name, price=price, url=url, photos=photos)


