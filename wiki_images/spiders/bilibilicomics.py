import scrapy
import os
import shutil
import requests
import json
from scrapy_splash import SplashRequest
from ..thread_pool import run_task
from concurrent.futures import wait

HOST = 'https://www.bilibilicomics.com'
URL_GET_ALL_DATA = f'{HOST}/twirp/comic.v1.Comic/GetImageIndex?device=pc&platform=web&lang=en&sys_lang=en'
URL_GET_TOKEN_IMG = f'{HOST}/twirp/comic.v1.Comic/ImageToken?device=pc&platform=web&lang=en&sys_lang=en'

def call_api(url, payload, headers, method):
    response = requests.request(method, url, headers=headers, data=payload)
    return json.loads(response.text)

def get_all_data(payload):
    url = URL_GET_ALL_DATA
    headers = {
        'content-type': 'application/json;charset=UTF-8'
    }
    return call_api(url, payload, headers, 'POST')

def get_token_img(path):
    url = URL_GET_TOKEN_IMG
    payload = "{\n    \"urls\": \"[\\\"" + f"{path}" + "@1000w.webp\\\"]\"\n}"
    headers = {
        'content-type': 'application/json;charset=UTF-8'
    }
    response = call_api(url, payload, headers, 'POST')
    print(response)
    return response['data'][0]

class BilibilicomicsSpider(scrapy.Spider):
    name = 'bilibilicomics'
    # start_urls = ['https://www.nettruyenus.com/truyen-tranh/ryuuma-no-gagou/chap-23/1050344']
    def __init__(self, dir='', link='', **kwargs):
        self.start_urls = [str(link)]  # py36
        self.dir = str(dir)
        super().__init__(**kwargs)  # python3
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )

    def parse(self, response):
        payload = {
            # "ep_id": self.dir,
            "ep_id": self.dir.split('-')[-1],
            "credential": ""
        }
        payload = json.dumps(payload)
        data = get_all_data(payload)
        mg_images = data['data']['images']
        raw_image_urls = []
        tasks = []
        for idx, mg_img in enumerate(mg_images):
            tasks.append(run_task(self.render_link_download, mg_img['path'], idx, raw_image_urls))
        wait(tasks)
        newlist = sorted(raw_image_urls, key=lambda d: d['idx']) 
        clean_image_urls=newlist
        tasks = []
        for item in clean_image_urls:
            cmd = f'mkdir -p local_folder/{self.name}/{self.dir}'
            os.system(cmd)
            tasks.append(run_task(self.download_img, item['url'], item['idx']))
        wait(tasks)
        shutil.make_archive(f'output_zip/{self.name}/{self.dir}', 'zip', f'local_folder/{self.name}/{self.dir}')
        cmd = f'rm -rf local_folder/{self.name}/{self.dir}'
        os.system(cmd)
        return
        # yield {
        #     'image_urls': clean_image_urls
        # }

    def render_link_download(self, path, idx, raw_image_urls):
        img_data = get_token_img(path)
        raw_image_urls.append(
            {
                "idx" : idx,
                "url" : f"{img_data['url']}?token={img_data['token']}"
            }
        )
    
    def download_img(self, url, idx):
        cmd = f'''
            curl '{url}' \
            --compressed --output local_folder/{self.name}/{self.dir}/{idx}.jpg
        '''
        os.system(cmd)
                   
