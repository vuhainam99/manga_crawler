import scrapy
import os
import shutil


class NettruyenusSpider(scrapy.Spider):
    name = 'nettruyenus'
    # start_urls = ['https://www.nettruyenus.com/truyen-tranh/ryuuma-no-gagou/chap-23/1050344']
    def __init__(self, dir='', link='', **kwargs):
        self.start_urls = [str(link)]  # py36
        self.dir = str(dir)
        super().__init__(**kwargs)  # python3
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        raw_image_urls = response.css('div.page-chapter ::attr(data-original)').getall()
        clean_image_urls=[]
        for img_url in raw_image_urls:
            clean_image_urls.append(response.urljoin(img_url))
        for idx, url in enumerate(clean_image_urls):
            cmd = f'mkdir -p local_folder/nettruyenus/{self.dir}'
            os.system(cmd)
            cmd = f'''
                curl '{url}' \
                -H 'Referer: https://www.nettruyenus.com/' \
                --compressed --output local_folder/nettruyenus/{self.dir}/{idx}.jpg
            '''
            os.system(cmd)
        shutil.make_archive(f'output_zip/nettruyenus/{self.dir}', 'zip', f'local_folder/nettruyenus/{self.dir}')
        cmd = f'rm -rf local_folder/nettruyenus/{self.dir}'
        os.system(cmd)
        return
        # yield {
        #     'image_urls': clean_image_urls
        # }
                   



