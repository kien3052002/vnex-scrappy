import scrapy


class VnExpressSpider(scrapy.Spider):
    name = 'vnex-spider'
    start_urls = ['https://vnexpress.net/kinh-doanh']

    def parse(self, response):
        categoryUrls = response.css('.ul-nav-folder li a::attr(href)').extract()
        for url in categoryUrls:
            if url != "" and url != 'https://ebox.vnexpress.net/':
                yield response.follow('https://vnexpress.net' + url, self.parse_category)

    def parse_category(self, response):
        newsLinks = response.css('#automation_TV0 > div > .item-news > .title-news > a::attr(href)').extract()
        for link in newsLinks:
            yield response.follow(link, self.parse_news)
    def parse_news(self, response):
        CATEGORY_SELECTOR = '.header-content > .breadcrumb > li:nth-child(2) > a::attr(title)'
        TITLE_SELECTOR = 'head > title::text'
        AUTHOR_SELECTOR = '.fck_detail > p.Normal:last-of-type > strong::text'
        DATE_SELECTOR = '.header-content .date::text'
        DESCRIPTION_SELECTOR = 'h1.title-detail::text'
        CONTENT_SELECTOR = ''

        yield {
            'source': response.request.url,
            'title': response.css(TITLE_SELECTOR).extract() ,
            'category': response.css(CATEGORY_SELECTOR).extract(),
            'author': response.css(AUTHOR_SELECTOR).extract(),
            'upload_date': response.css(DATE_SELECTOR).extract(),
            'description': response.css(DESCRIPTION_SELECTOR).extract(),
            # 'content': response.css(CONTENT_SELECTOR).extract(),
        }







