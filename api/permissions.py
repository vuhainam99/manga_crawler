from api.models.ip_restriction import IPRestriction
from rest_framework import permissions

class IPRestrictionPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        def get_client_ip(request):
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            return ip
        remote_addr = get_client_ip(request)
        for restriction in IPRestriction.objects.all():
            r: IPRestriction = restriction
            if r.type == 'match' and r.ip_or_domain == remote_addr:
                return True
        return False
