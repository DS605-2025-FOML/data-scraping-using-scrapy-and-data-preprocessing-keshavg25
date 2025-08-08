import scrapy
from ..items import BookItem

class BookSpider(scrapy.Spider):
    name = 'book_spider'
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            item = BookItem()
            item['title'] = book.css('h3 a::attr(title)').extract_first()
            item['price'] = book.css('p.price_color::text').extract_first()
            item['rating'] = book.css('p.star-rating::attr(class)').extract()[-1].split()[-1]
            item['availability'] = book.css('p.instock.availability::text').extract()
            item['availability'] = ''.join(item['availability']).strip()
            yield item

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)