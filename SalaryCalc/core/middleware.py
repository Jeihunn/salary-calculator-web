from django.utils import timezone
from identity.models import Blacklist
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse
from django.template import loader


class AddUserIpsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            ip_address = self.get_client_ip(request)

            if not request.user.ips:
                request.user.ips = []

            if ip_address not in request.user.ips:
                request.user.ips.append(ip_address)
                request.user.save()
        return None

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class BlacklistMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = request.user
        ip_address = self.get_client_ip(request)

        blacklist_entry = Blacklist.objects.filter(
            ip_address=ip_address, is_active=True).first()

        if not blacklist_entry:
            if user.is_authenticated:
                blacklist_entry = Blacklist.objects.filter(
                    user=user, is_active=True).first()

        if blacklist_entry:
            if timezone.now() > blacklist_entry.start_time:
                if timezone.now() < blacklist_entry.start_time + blacklist_entry.duration:
                    if user.is_authenticated:
                        return self.blocked_response(request, "user-based")
                    else:
                        return self.blocked_response(request, "IP-based")
                else:
                    blacklist_entry.is_active = False
                    blacklist_entry.save()

        return None

    def blocked_response(self, request, block_type):
        template = loader.get_template('identity/blacklist.html')
        context = {'block_type': block_type}
        return HttpResponse(template.render(context, request))

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
