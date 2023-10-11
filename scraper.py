import psycopg2
import scrapy
from database import Database
from items import NewsItem


class VnExpressSpider(scrapy.Spider):
    name = 'vnex-spider'
    start_urls = ['https://vnexpress.net/kinh-doanh']

    def parse(self, response):

        CATEGORY_SELECTOR = '.ul-nav-folder li a::attr(href)'

        category_urls = response.css(CATEGORY_SELECTOR).extract()
        for url in category_urls:
            if url and url != 'https://ebox.vnexpress.net/':
                yield response.follow('https://vnexpress.net' + url, self.parse_category)


    def parse_category(self, response):
        NEWS_SELECTOR = '#automation_TV0 > div > .item-news > .title-news > a::attr(href)'

        news_links = response.css(NEWS_SELECTOR).extract()
        if len(news_links) > 0:
            for link in news_links:
                yield response.follow(link, self.parse_news)

            next_page = response.css('a.btn-page.next-page::attr(href)').get()
            if next_page:
                yield response.follow(next_page, self.parse_category)

    def parse_news(self, response):
        ID_SELECTOR = 'head meta[name=tt_article_id]::attr(content)'
        CATEGORY_SELECTOR = 'head meta[itemprop=articleSection]::attr(content)'
        TITLE_SELECTOR = 'head title::text'
        AUTHOR_SELECTOR = '.fck_detail > p.Normal:last-of-type > strong::text, .fck_detail > p.author_mail > strong::text'
        PUBLISH_DATE_SELECTOR = 'head meta[name=pubdate]::attr(content)'
        LAST_MOD_SELECTOR = 'head meta[name=lastmod]::attr(content)'
        DESCRIPTION_SELECTOR = 'head meta[name=description]::attr(content)'
        CONTENT_SELECTOR = '.container article.fck_detail'

        news_item = NewsItem()
        news_item['id'] = response.css(ID_SELECTOR).get()
        news_item['source'] = response.request.url
        news_item['title'] = response.css(TITLE_SELECTOR).get()
        news_item['category'] = response.css(CATEGORY_SELECTOR).get()
        news_item['author'] = response.css(AUTHOR_SELECTOR).get()
        news_item['publish_date'] = response.css(PUBLISH_DATE_SELECTOR).get()
        news_item['last_mod'] = response.css(LAST_MOD_SELECTOR).get()
        news_item['description'] = response.css(DESCRIPTION_SELECTOR).get()
        news_item['content'] = response.css(CONTENT_SELECTOR).get()

        yield news_item

        db = Database()
        db.insert_news(news_item)








