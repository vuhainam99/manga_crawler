from django.contrib import admin

# Register your models here.
from api.models.ip_restriction import IPRestriction
from api.models.crawl_link import CrawlLink


class IPRestrictionAdmin(admin.ModelAdmin):
    list_display = ['id','ip_or_domain', 'type', 'title']
    list_editable = ['ip_or_domain', 'type', 'title']

admin.site.register(IPRestriction, IPRestrictionAdmin)

class CrawlLinkAdmin(admin.ModelAdmin):
    list_display = ['id','link', 'status', 'output_path', 'download_at']
    list_editable = []

admin.site.register(CrawlLink, CrawlLinkAdmin)


