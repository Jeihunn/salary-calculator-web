from django.contrib.sitemaps import Sitemap
from django.urls import reverse_lazy


class IndexViewSitemap(Sitemap):
    priority = 1.0
    changefreq = "weekly"
    protocol = "https"

    def items(self):
        return ["core:index_view"]

    def location(self, item):
        return reverse_lazy(item)


class OtherPageSitemap(Sitemap):
    priority = 0.8
    changefreq = "weekly"
    protocol = "https"

    def items(self):
        return [
            "account_login",
            "account_signup",
            "core:faq_view",
            "core:contact_view",
            "core:groos_to_nett_view",
            "core:nett_to_gross_view",
            "core:work_calendar_view",
        ]

    def location(self, item):
        return reverse_lazy(item)
