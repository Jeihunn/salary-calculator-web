from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from core.models import AbstractModel
from django.utils.translation import gettext_lazy as _


# Create your models here.


class User(AbstractUser):
    ips = models.JSONField(verbose_name=_("IP'lər"), default=list, null=True, blank=True)