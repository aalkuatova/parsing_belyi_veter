
BOT_NAME = 'veter'
SPIDER_MODULES = ['veter.spiders']
NEWSPIDER_MODULE = 'veter.spiders'
# ROTATING_PROXY_LIST = [
#   "https://0Bb7Tp:KGUFPk@45.129.7.7:8000",
#   "https://0Bb7Tp:KGUFPk@45.129.7.156:8000",
#   "https://0Bb7Tp:KGUFPk@45.129.7.178:8000",
#   "https://0Bb7Tp:KGUFPk@45.129.6.155:8000",
#   "https://0Bb7Tp:KGUFPk@45.129.6.101:8000",
#   "https://0Bb7Tp:KGUFPk@45.129.5.7:8000"
# ]

USER_AGENT = [
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36']
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 5
DOWNLOAD_DELAY = 0.2
COOKIES_ENABLED = False

DEFAULT_REQUEST_HEADERS = {
  'Accept': '*/*',
  'Accept-Encoding': 'gzip, deflate, br',
  'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',

}
#Enable this if u use proxy list above
# DOWNLOADER_MIDDLEWARES = {
#   'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
#   'rotating_proxies.middlewares.BanDetectionMiddleware': 620}


ITEM_PIPELINES = {
   'veter.pipelines.VeterPipeline': 1
}

# ITEM_PIPELINES = {'scrapy.pipelines.images.ImagesPipeline': 1}

IMAGES_STORE = 'images_folder'

FEED_EXPORT_ENCODING = 'utf-8'
FEED_EXPORT_FIELDS = ['high_category',
                      'middle_category',
                      'small_category',
                      'sku',
                      'name',
                      'prod_url',
                      'price',
                      'description',
                      'properties',
                      'image_urls',
                      'image_link']
