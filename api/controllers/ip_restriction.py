from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action


from api.models.ip_restriction import IPRestriction

class IPRestrictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPRestriction
        fields = [
            'id', 'title', 'ip_or_domain', 'type',
        ]

class IPRestrictionViewSet(viewsets.ModelViewSet):
    serializer_class = IPRestrictionSerializer
    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.action == 'retrieve' or self.action == 'list':
            serializer_class = self.serializer_class
        return serializer_class
    def get_queryset(self):
        queryset = IPRestriction.objects.all()
        return queryset