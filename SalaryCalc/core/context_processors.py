from .models import (
    SiteInfo,
    CalculationCount
)

def site_info_global(request):
    site_info_global = SiteInfo.objects.filter(is_active=True).last()
    return {
        "site_info_global": site_info_global,
    }

def calculation_count_global(request):
    calculation_count = CalculationCount.objects.first()
    return {
        "calculation_count_global": calculation_count,
    }