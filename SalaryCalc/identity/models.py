from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.


class User(AbstractUser):
    ips = models.JSONField(
        verbose_name=_("IP-lər"),
        default=list,
        null=True,
        blank=True
    )


class Blacklist(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("İstifadəçi")
    )

    ip_address = models.GenericIPAddressField(
        verbose_name=_("IP ünvanı"),
        protocol="both",
        unpack_ipv4=False,
        null=True,
        blank=True
    )
    start_time = models.DateTimeField(
        verbose_name=_("Başlama vaxtı"),
        default=timezone.now
    )
    duration = models.DurationField(
        verbose_name=_("Müddət"),
        help_text=_("Müddəti '45 days 15:29:40' formatında göstərin."),
    )
    reason = models.TextField(
        verbose_name=_("Səbəb"),
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        verbose_name=_("Aktiv"),
        default=True
    )
    created_at = models.DateTimeField(
        verbose_name=_("Yaradılma vaxtı"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Yenilənmə vaxtı"),
        auto_now=True
    )

    def __str__(self):
        if self.user:
            return f"Blacklist for {self.user.username}"
        elif self.ip_address:
            return f"Blacklist for IP {self.ip_address}"

    class Meta:
        verbose_name = _("Qara siyahı girişi")
        verbose_name_plural = _("Qara siyahı girişləri")
