import scrapy
from vnexscrapy.items import CategoryItem
from vnexscrapy.pipelines import DatabasePipeline
from urllib.parse import urlparse


class CategorySpider(scrapy.Spider):
    name = 'category_spider'
    start_urls = ['https://vnexpress.net/kinh-doanh']
    selectors = None
    db = None

    def __init__(self, *args, **kwargs):
        super(CategorySpider, self).__init__(*args, **kwargs)
        self.db = DatabasePipeline()

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse)

    def parse(self, response):
        domain = urlparse(response.request.url).netloc

        self.selectors = self.db.get_data('config', f"domain = '{domain}'")
        print(self.selectors)

        # lấy danh sách url các category
        category_urls = response.css(self.selectors['category_url_list_selector']).extract()

        # vào từng url cụ thể
        for url in category_urls:
            if url and url != 'https://ebox.vnexpress.net/':
                yield response.follow('https://vnexpress.net' + url, self.parse_category)

    def parse_category(self, response):

        selectors = self.selectors

        # lấy id và title của category
        category_item = CategoryItem()
        category_item['id'] = response.css(selectors['category_id_selector']).get()
        category_item['title'] = response.css(selectors['category_title_selector']).get().split(',')[2]

        yield category_item
