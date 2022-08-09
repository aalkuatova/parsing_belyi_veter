import scrapy


class VeterItem(scrapy.Item):
    
    
    high_category = scrapy.Field()
    middle_category = scrapy.Field()
    small_category = scrapy.Field()
    sku = scrapy.Field()
    prod_link = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    properties = scrapy.Field()
    image_urls = scrapy.Field()
    image_link = scrapy.Field()
   
    