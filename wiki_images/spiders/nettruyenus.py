import scrapy
import os
import shutil
from scrapy_splash import SplashRequest 

class NettruyenusSpider(scrapy.Spider):
    name = 'nettruyenus'
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
        # chapter_links = response.css('div.chapter a::attr(href)').extract()
        # print(chapter_links)
        # return
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
                   


# command = """
#     curl 'https://www.nettruyenus.com/Comic/Services/ComicService.asmx/ProcessChapterList?comicId=4188' \
#     -H 'authority: www.nettruyenus.com' \
#     -H 'accept: */*' \
#     -H 'accept-language: en-US,en;q=0.9' \
#     -H 'content-type: application/x-www-form-urlencoded' \
#     -H 'sec-ch-ua: "Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"' \
#     -H 'sec-ch-ua-mobile: ?0' \
#     -H 'sec-ch-ua-platform: "macOS"' \
#     -H 'sec-fetch-dest: empty' \
#     -H 'sec-fetch-mode: cors' \
#     -H 'sec-fetch-site: same-origin' \
#     -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36' \
#     --compressed
# """

# output = os.popen(command).read()