from scrapy.pipelines.images import ImagesPipeline
import urllib

class VeterPipeline(ImagesPipeline):
    def process_item(self, item, spider):
        for number,image_url in enumerate(item['image_urls'],start = 1):
            # the right path should be added to folder
            urllib.request.urlretrieve(image_url, f"/Users/aziza/Desktop/belyi_veter_scraper_code/images_folder/{item['sku']}_{str(number)}.jpg")
        return item



