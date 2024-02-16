import scrapy
import os
import shutil
import json
from scrapy_splash import SplashRequest 
from ..thread_pool import run_task
from concurrent.futures import wait


class ComickSpider(scrapy.Spider):
    name = 'comick'
    # start_urls = ['https://www.nettruyenus.com/truyen-tranh/ryuuma-no-gagou/chap-23/1050344']
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
        img_elements = response.css('script#__NEXT_DATA__ ::text').get()
        data = json.loads(img_elements)
        build_id = data['buildId']
        md_images = data['props']['pageProps']['chapter']['md_images']
        for md_img in md_images:
            # Extract the value of the "data-src" attribute
            data_src_value = 'https://meo.comick.pictures/' + md_img['b2key']
            raw_image_urls.append(data_src_value)
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
                   
