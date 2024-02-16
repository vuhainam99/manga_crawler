import scrapy
import os
import shutil
from ..thread_pool import run_task
from concurrent.futures import wait


class BaozimhSpider(scrapy.Spider):
    name = 'baozimh'
    # start_urls = ['https://www.nettruyenus.com/truyen-tranh/ryuuma-no-gagou/chap-23/1050344']
    def __init__(self, dir='', link='', **kwargs):
        self.start_urls = [str(link)]  # py36
        self.dir = str(dir)
        super().__init__(**kwargs)  # python3
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        raw_image_urls = []
        img_elements = response.css('img')
        for img in img_elements:
            # Extract the value of the "data-src" attribute
            data_src_value = img.attrib['src']
            raw_image_urls.append(data_src_value)
        clean_image_urls=[]
        for img_url in raw_image_urls:
            clean_image_urls.append(response.urljoin(img_url))
        tasks = []
        for idx, url in enumerate(clean_image_urls):
            cmd = f'mkdir -p local_folder/{self.name}/{self.dir}'
            os.system(cmd)
            tasks.append(run_task(self.download_img, url, idx))
        wait(tasks)
        shutil.make_archive(f'output_zip/{self.name}/{self.dir}', 'zip', f'local_folder/{self.name}/{self.dir}')
        cmd = f'rm -rf local_folder/{self.name}/{self.dir}'
        os.system(cmd)
        return
        # yield {
        #     'image_urls': clean_image_urls
        # }

    def download_img(self, url, idx):
        cmd = f'''
            curl '{url}' \
            --compressed --output local_folder/{self.name}/{self.dir}/{idx}.jpg
        '''
        os.system(cmd)
                   
