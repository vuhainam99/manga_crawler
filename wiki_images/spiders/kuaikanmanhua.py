import scrapy
import os
import re
import json
import shutil
from scrapy_splash import SplashRequest
from ..thread_pool import run_task
from concurrent.futures import wait


class KuaikanmanhuaSpider(scrapy.Spider):
    name = 'kuaikanmanhua'

    def __init__(self, dir='', link='', **kwargs):
        self.start_urls = [str(link)]  # py36
        self.dir = str(dir)
        super().__init__(**kwargs)  # python3
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, 
                endpoint='render.html', 
                args={'wait': 0.5}, 
            )

    def parse(self, response):
        raw_image_urls = []
        elements = response.css('script ::text').getall()
        data_string = None
        for element in elements:
            # Extract the value of the "data-src" attribute
            if 'window.__NUXT__=' in element:
                data_string = element.split('}}}}')[-1].split(');')[0]
        items = json.loads((data_string.replace('(', '[').replace(')',']').replace('Array','')))
        for item in items:
            if isinstance(item, str) and 'https://' in item and 'image' in item and 'sign=' in item:
                raw_image_urls.append(item)
        clean_image_urls=raw_image_urls
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
                   



