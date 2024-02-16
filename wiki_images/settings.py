
BOT_NAME = 'wiki_images'

SPIDER_MODULES = ['wiki_images.spiders']
NEWSPIDER_MODULE = 'wiki_images.spiders'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
SPLASH_URL = 'http://splash:8050/'
DOWNLOADER_MIDDLEWARES = { 
    'scrapy_splash.SplashCookiesMiddleware': 723, 
    'scrapy_splash.SplashMiddleware': 725, 
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810, 
}
SPIDER_MIDDLEWARES = { 
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100, 
}
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter' 
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

ITEM_PIPELINES = {'wiki_images.pipelines.CustomWikiImagesPipeline': 1}
IMAGES_STORE = 'local_folder'

ROBOTSTXT_OBEY = True
