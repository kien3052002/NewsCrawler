from scrapy.item import Item, Field


class NewsItem(Item):
    id = Field()
    title = Field()
    source_id = Field()
    category_id = Field()
    author = Field()
    description = Field()
    content_html = Field()
    content_text = Field()
    keywords = Field()


class CategoryItem(Item):
    id = Field()
    title = Field()

class SourceItem(Item):
    id = Field()
    url = Field()
    title = Field()
    domain = Field()
    publish_date = Field()
    last_mod = Field()
    author = Field()
