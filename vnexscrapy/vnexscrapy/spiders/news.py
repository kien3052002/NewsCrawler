import scrapy
from vnexscrapy.items import NewsItem, SourceItem
from vnexscrapy.pipelines import DatabasePipeline
from urllib.parse import urlparse


class NewsSpider(scrapy.Spider):
    name = 'news_spider'
    start_urls = ['https://vnexpress.net/kinh-doanh']
    selectors = None
    db = DatabasePipeline()

    def __init__(self, *args, **kwargs):
        super(NewsSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

    def parse(self, response):

        domain = urlparse(response.request.url).netloc
        self.selectors = self.db.get_data('config', f"domain = '{domain}'")

        # lấy url từng category
        category_urls = response.css(self.selectors['category_url_list_selector']).extract()

        # truy cập từng category để lấy news
        for url in category_urls:
            if url and url != 'https://ebox.vnexpress.net/':
                yield response.follow('https://vnexpress.net' + url, self.parse_category)

    def parse_category(self, response):

        # lấy danh sách link các news
        news_links = response.css(self.selectors['news_from_list_selector']).extract()

        # lấy category_id của các news trong danh sách vừa lấy
        category_id = response.css(self.selectors['category_id_selector']).get()
        if len(news_links) > 0:

            # truy cập từng link, truyền category_id vừa lấy
            for link in news_links:
                yield response.follow(link, self.parse_news, cb_kwargs={'category_id': category_id})

            # sang trang tiếp theo của cùng category
            next_page = response.css(self.selectors['next_page_selector']).get()
            if next_page:
                yield response.follow(next_page, self.parse_category)

    def parse_news(self, response, category_id):

        source_item = SourceItem()
        selectors = self.selectors

        source_item['id'] = response.css(selectors['news_id_selector']).get()
        source_item['url'] = response.request.url
        source_item['domain'] = selectors['domain']
        source_item['title'] = response.css(selectors['news_title_selector']).get()
        source_item['publish_date'] = response.css(selectors['publish_date_selector']).get()
        source_item['last_mod'] = response.css(selectors['last_mod_selector']).get()
        source_item['author'] = response.css(selectors['author_selector']).get()

        yield source_item

        news_item = NewsItem()

        news_item['id'] = response.css(selectors['news_id_selector']).get()
        news_item['title'] = response.css(selectors['news_title_selector']).get()
        news_item['source_id'] = response.css(selectors['news_id_selector']).get()
        news_item['category_id'] = category_id
        news_item['author'] = response.css(selectors['author_selector']).get()
        news_item['description'] = response.css(selectors['description_selector']).get()
        news_item['content_html'] = response.css(selectors['content_html_selector']).get()
        news_item['content_text'] = " ".join(response.css(selectors['content_text_selector']).getall())
        news_item['keywords'] = response.css(selectors['keywords_selector']).get()

        yield news_item
