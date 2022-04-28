import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BooksInfoSpider(CrawlSpider):
    name = 'books_info'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//li[@class='next']/a"), follow=True),
        Rule(LinkExtractor(restrict_xpaths=".//article/div[@class='image_container']/a"), callback='parse_item', follow=True)
    )

    def parse_item(self, response):
        item = {}
        item['title'] = response.xpath("//div[contains(@class, 'product_main')]/h1/text()").get()
        item['price'] = response.xpath("//p[@class='price_color']/text()").get()
        item['description'] = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get()
        return item
