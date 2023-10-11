
from scrapy.item import Item, Field

class NewsItem(Item):
    id = Field()
    source = Field()
    title = Field()
    category = Field()
    author = Field()
    publish_date = Field()
    last_mod = Field()
    description = Field()
    content = Field()
