from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import permissions
from django.db import transaction
from django.http import FileResponse

import os

OUTPUT_FOLDER = 'output_zip'




from api.models.crawl_link import CrawlLink

class CrawlLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlLink
        fields = [
            'id', 'link', 'status', 'output_path'
        ]
        read_only_fields = [
            'id', 'status', 'output_path'
        ]

    def create(self, validated_data):
        validated_data['status'] = CrawlLink.Status.WAITING
        link = validated_data['link']
        if "nettruyenss.com" in link:
            id_source = link.split('/')[-1]
            output_path = f'nettruyenus/{id_source}'
            link_ex = CrawlLink.objects.filter(output_path=output_path).first()
            if link_ex:
                return link_ex
            cmd = f'scrapy crawl nettruyenus -a dir={id_source} -a link={link}'
        elif "dzmanga.com" in link: #site baozimh
            id_source = '-'.join(link.split('/')[-2:]).replace('.html', '')
            output_path = f'baozimh/{id_source}'
            link_ex = CrawlLink.objects.filter(output_path=output_path).first()
            if link_ex:
                return link_ex
            cmd = f'scrapy crawl baozimh -a dir={id_source} -a link={link}'
        elif "comick.app" in link: #site comick
            id_source = '-'.join(link.split('/')[-2:])
            output_path = f'comick/{id_source}'
            link_ex = CrawlLink.objects.filter(output_path=output_path).first()
            if link_ex:
                return link_ex
            cmd = f'scrapy crawl comick -a dir={id_source} -a link={link}'
        elif "bilibilicomics.com" in link: #site comick
            id_source = '-'.join(link.split('?')[0].split('/')[-2:])
            output_path = f'bilibilicomics/{id_source}'
            link_ex = CrawlLink.objects.filter(output_path=output_path).first()
            if link_ex:
                return link_ex
            cmd = f'scrapy crawl bilibilicomics -a dir={id_source} -a link={link}'
        elif "kuaikanmanhua.com" in link: #site comick
            id_source = link.split('/')[-2]
            output_path = f'kuaikanmanhua/{id_source}'
            link_ex = CrawlLink.objects.filter(output_path=output_path).first()
            if link_ex:
                return link_ex
            cmd = f'scrapy crawl kuaikanmanhua -a dir={id_source} -a link={link}'
        else:
            raise serializers.ValidationError("domain not suport")
        with transaction.atomic():
            obj = super().create(validated_data)
            obj.save()
            link = obj.link
            obj.output_path = output_path  
            os.system(cmd)
            obj.status = CrawlLink.Status.COMPLETE
            obj.save()
            return obj

class CrawlLinkViewSet(viewsets.ModelViewSet):
    serializer_class = CrawlLinkSerializer
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == 'retrieve' or self.action == 'list':
            serializer_class = self.serializer_class
        return serializer_class
    def get_queryset(self):
        queryset = CrawlLink.objects.all()
        return queryset