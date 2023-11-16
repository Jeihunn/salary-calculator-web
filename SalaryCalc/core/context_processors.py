from .models import SiteInfo

def site_info_global(request):
    site_info_global = SiteInfo.objects.filter(is_active=True).last()
    return {
        "site_info_global": site_info_global,
    }