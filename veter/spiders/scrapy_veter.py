
import scrapy
from veter.items import VeterItem
import json
class mechtaSpider(scrapy.Spider):
    name = "belveter"
    allowed_domains = ['shop.kz']

    def start_requests(self):
        urls = [
            'https://shop.kz/catalog/smartfony-i-gadzhety/',
            'https://shop.kz/catalog/komplektuyushchie/',
            'https://shop.kz/catalog/noutbuki-i-kompyutery/',
            'https://shop.kz/catalog/kompyuternaya-periferiya/',
            'https://shop.kz/catalog/orgtekhnika-i-raskhodnye-materialy/',
            'https://shop.kz/catalog/setevoe-i-servernoe-oborudovanie/',
            'https://shop.kz/catalog/televizory-audio-video/',
            'https://shop.kz/catalog/bytovaya-tekhnika-i-tovary-dlya-doma/',
            'https://shop.kz/catalog/tovary-dlya-geymerov/',
            'https://shop.kz/catalog/razvlecheniya-i-otdykh/',
            'https://shop.kz/catalog/avtotovary/',
            'https://shop.kz/catalog/kantstovary/',
            'https://shop.kz/catalog/sumki/'
               ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, meta = {
                  'dont_redirect': True,
                  'handle_httpstatus_list': [302]
              })
            
    def parse(self,response):
        item = VeterItem() 
        item['high_category'] = response.css('h1.bx-title.dbg_title::text').get()
        for cats in response.css('h2.bx_catalog_tile_title'):
            high_urls = cats.css('a::attr(href)').get()
            item['middle_category'] = cats.css('a::text').get()
            yield response.follow(url=f"https://shop.kz{high_urls}", callback = self.parse_second, meta={'high_category': item['high_category'],'middle_category': item['middle_category']})
    
    def parse_second(self,response):
        item = VeterItem() 
        item['high_category'] = response.meta.get('high_category')
        item['middle_category'] = response.meta.get('middle_category')
        for cats in response.css('h2.bx_catalog_tile_title'):
            middle_urls = cats.css('a::attr(href)').get()
            item['small_category'] = cats.css('a::text').get()
            yield response.follow(middle_urls, callback = self.open_items, meta={'high_category': item['high_category'],'middle_category': item['middle_category'],'small_category': item['small_category']})

    def open_items(self,response):
        item = VeterItem()
        item['high_category'] = response.meta.get('high_category')
        item['middle_category'] = response.meta.get('middle_category')
        item['small_category'] = response.meta.get('small_category')
        for link in response.css('div.bx_catalog_item_title a::attr(href)'):
            item['prod_link'] = "https://shop.kz" + link.get()
            yield response.follow(item['prod_link'], callback = self.parse_item, meta={'high_category': item['high_category'],'small_category': item['small_category'],'middle_category': item['middle_category'],'prod_link': item['prod_link']})
        
        next_page = response.css('li.bx-pag-next a::attr(href)').get()
        if next_page is not None:
            url= "https://shop.kz"+next_page
            yield response.follow(url, callback=self.open_items,meta={'high_category': item['high_category'],'small_category': item['small_category'],'middle_category': item['middle_category']})
    
    def parse_item(self, response):
        item = VeterItem()            
        item['high_category'] = response.meta.get('high_category')
        item['middle_category'] = response.meta.get('middle_category')
        item['small_category'] = response.meta.get('small_category')
        item['prod_link'] = response.meta.get('prod_link')

        item['description'] = response.css('div.bx_item_description').css('::text').getall()[3:]
        if item['description'] is not None:
            opis_j = "".join(item['description'])
            opis_j = opis_j.replace('\n','').strip()
            opis_j = opis_j.replace('\t','').strip()
            opis_j = opis_j.replace('\r','').strip()
            item['description'] = opis_j
      
        script = response.xpath("//script[@type='application/ld+json']/text()").get()
        js = json.loads(script)
        d = {}
        the_name = js['name']
        if '&amp;quot;' not in the_name:
            item['name'] = the_name
        else:
            item['name'] = the_name.replace('&amp;quot;','"').strip()
        item['sku'] = js['mpn']
        the_price = response.css('div.item_current_price::text').get()
        if the_price is not None:
            item['price'] = the_price.replace('₸','').strip()
        else:
            item['price'] = ''
        properties = response.css('div.bx_detail_chars_i')
        for descr in properties:
            key = descr.css('span.glossary-term::text').get()
            value = descr.css('dd.bx_detail_chars_i_field::text').get()
            d[key] = value
        item['properties'] = d
        
        item['image_urls'] = js['image']
        item['image_link'] = [item['sku']+ '_' + str(index) + '.jpg' for index, x in enumerate(item['image_urls'], start = 1)]
        yield item

        







#------------------------Main version -----------------

    # def start_requests(self):
        
    #     urls = ['https://shop.kz/catalog/smartfony-i-gadzhety/',
    #             'https://shop.kz/catalog/komplektuyushchie/',
    #             'https://shop.kz/catalog/noutbuki-i-kompyutery/',
    #             'https://shop.kz/catalog/kompyuternaya-periferiya/',
    #             'https://shop.kz/catalog/orgtekhnika-i-raskhodnye-materialy/',
    #             'https://shop.kz/catalog/setevoe-i-servernoe-oborudovanie/',
    #             'https://shop.kz/catalog/televizory-audio-video/',
    #             'https://shop.kz/catalog/bytovaya-tekhnika-i-tovary-dlya-doma/',
    #             'https://shop.kz/catalog/tovary-dlya-geymerov/',
    #             'https://shop.kz/catalog/razvlecheniya-i-otdykh/',
    #             'https://shop.kz/catalog/avtotovary/',
    #             'https://shop.kz/catalog/kantstovary/',
    #             'https://shop.kz/catalog/sumki/'
    #            ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse, meta = {
    #               'dont_redirect': True,
    #               'handle_httpstatus_list': [302]
    #           })
            

    # def parse(self,response):
    #     categories = response.css('h2.bx_catalog_tile_title a::attr(href)').getall()
    #     for cats in categories:
    #         yield response.follow(url=f"https://shop.kz{cats}", callback = self.parse_second)

    # def parse_second(self,response):
    #     item = VeterItem() 
    #     small_categories = response.css('h2.bx_catalog_tile_title')
    #     for cat in small_categories:
    #         link_cat = cat.css('a::attr(href)').get()
    #         yield response.follow(link_cat, callback = self.open_items)

    # def open_items(self,response):
    #     item = VeterItem() 
    #     item['category'] = response.css('h1.bx-title.dbg_title::text').get()
    #     for link in response.css('div.bx_catalog_item_title a::attr(href)'):
    #         item['prod_link'] = "https://shop.kz" + link.get()
    #         yield response.follow("https://shop.kz"+link.get(), callback = self.parse_item, meta={'prod_link': item['prod_link'],
    #                                                                                                 'category':item['category']})

    #     next_page = response.css('li.bx-pag-next a::attr(href)').get()
    #     if next_page is not None:
    #         url= "https://shop.kz"+next_page
    #         yield response.follow(url, callback=self.open_items)

    # def parse_item(self, response):
    #     item = VeterItem()            

    #     script = response.xpath("//script[@type='application/ld+json']/text()").get()
    #     js = json.loads(script)
    #     d = {}
    #     description = response.css('div.bx_detail_chars_i')
    #     for descr in description:
    #         key = descr.css('span.glossary-term::text').get()
    #         value = descr.css('dd.bx_detail_chars_i_field::text').get()
    #         d[key] = value
    #     item['category'] = response.meta.get('category')
    #     item['name'] = js['name']
    #     item['price'] = response.css('div.item_current_price::text').get()
    #     item['sku'] = js['mpn']
    #     item['image_urls'] = js['image']
    #     item['description'] = d
    #     item['prod_link'] = response.meta.get('prod_link')
    #     yield item 

# Have to fix prices, if price is None 
# Have to fix categories