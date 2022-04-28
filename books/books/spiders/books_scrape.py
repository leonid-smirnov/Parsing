import scrapy

class BooksScrapeSpider(scrapy.Spider):
    name = 'books_scrape'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/']

    def parse(self, response):
        articles = response.xpath("//article")
        for article in articles:
            yield {
                'title': article.xpath(".//h3/a/@title").get(),
                'image': response.urljoin(article.xpath(".//div[@class='image_container']/a/img/@src").get()),
                'price': article.xpath(".//p[@class='price_color']/text()").get()
            }

        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)
