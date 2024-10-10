from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField
from django.utils.html import strip_tags
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.


class CustomImageField(models.ImageField):
    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        if not value.name.isascii():
            raise ValidationError(_("Şəklin adı '{}' ASCII olmayan simvolları ehtiva edir. Şəklin adında yalnız əsas ingilis hərfləri (A-Z, a-z), rəqəmlər və xüsusi simvollar ola bilər. Lütfən, düzgün şəkil adı daxil edin.").format(value.name))


class Year(models.Model):
    year_value = models.PositiveSmallIntegerField(
        verbose_name=_("İl"),
        unique=True
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
        return str(self.year_value)

    class Meta:
        verbose_name = _("İl")
        verbose_name_plural = _("İllər")


class Month(models.Model):
    name = models.CharField(
        verbose_name=_("Ay adı"),
        max_length=20,
        unique=True
    )
    month_number = models.PositiveSmallIntegerField(
        verbose_name=_("Ay nömrəsi"),
        unique=True,
        validators=[MinValueValidator(1), MaxValueValidator(12)]
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
        return f"{self.name} ({self.month_number})"

    class Meta:
        verbose_name = _("Ay")
        verbose_name_plural = _("Aylar")


class Shift(models.Model):
    name = models.CharField(
        verbose_name=_("Növbə adı"),
        max_length=20,
        unique=True
    )
    value = models.CharField(
        verbose_name=_("Növbə dəyəri"),
        max_length=1,
        unique=True
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
        return f"{self.name} ({self.value})"

    class Meta:
        verbose_name = _("Növbə")
        verbose_name_plural = _("Növbələr")


class WorkCalendar(models.Model):
    year = models.ForeignKey(
        Year, on_delete=models.CASCADE,
        verbose_name=_("İl")
    )
    month = models.ForeignKey(
        Month, on_delete=models.CASCADE,
        verbose_name=_("Ay")
    )

    monthly_work_hour = models.PositiveSmallIntegerField(
        verbose_name=_("İstehsalat təqviminə uyğun aylıq iş norması"),
    )
    group_a_general_work_hour = models.PositiveSmallIntegerField(
        verbose_name=_("Ümumi iş saatı (A)"),
    )
    group_a_daytime_work_hour = models.PositiveSmallIntegerField(
        verbose_name=_("Gündüz iş saatı (A)"),
    )
    group_a_nighttime_work_hour = models.PositiveSmallIntegerField(
        verbose_name=_("Gecə iş saatı (A)"),
    )
    group_a_holiday_work_hour = models.PositiveSmallIntegerField(
        verbose_name=_("Bayram iş saatı (A)"),
    )
    group_b_general_work_hour = models.PositiveSmallIntegerField(
        verbose_name=_("Ümumi iş saatı (B)"),
    )
    group_b_daytime_work_hour = models.PositiveSmallIntegerField(
        verbose_name=_("Gündüz iş saatı (B)"),
    )
    group_b_nighttime_work_hour = models.PositiveSmallIntegerField(
        verbose_name=_("Gecə iş saatı (B)"),
    )
    group_b_holiday_work_hour = models.PositiveSmallIntegerField(
        verbose_name=_("Bayram iş saatı (B)"),
    )
    group_c_general_work_hour = models.PositiveSmallIntegerField(
        verbose_name=_("Ümumi iş saatı (C)"),
    )
    group_c_daytime_work_hour = models.PositiveSmallIntegerField(
        verbose_name=_("Gündüz iş saatı (C)"),
    )
    group_c_nighttime_work_hour = models.PositiveSmallIntegerField(
        verbose_name=_("Gecə iş saatı (C)"),
    )
    group_c_holiday_work_hour = models.PositiveSmallIntegerField(
        verbose_name=_("Bayram iş saatı (C)"),
    )
    group_d_general_work_hour = models.PositiveSmallIntegerField(
        verbose_name=_("Ümumi iş saatı (D)"),
    )
    group_d_daytime_work_hour = models.PositiveSmallIntegerField(
        verbose_name=_("Gündüz iş saatı (D)"),
    )
    group_d_nighttime_work_hour = models.PositiveSmallIntegerField(
        verbose_name=_("Gecə iş saatı (D)"),
    )
    group_d_holiday_work_hour = models.PositiveSmallIntegerField(
        verbose_name=_("Bayram iş saatı (D)"),
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
        return str(f"{self.year} - {self.month}")

    @classmethod
    def get_years_list(cls):
        return cls.objects.values_list("year__year_value", flat=True).distinct().order_by("-year__year_value")

    @classmethod
    def get_work_calendar_data(cls):
        work_calendar_data = {}

        years = cls.get_years_list()

        for year in years:
            year_data = {}
            if WorkCalendarImage.objects.filter(year__year_value=year).exists():
                year_data["image"] = WorkCalendarImage.objects.get(
                    year__year_value=year).image.url
            else:
                year_data["image"] = None
            months = range(1, 13)

            for month in months:
                if cls.objects.filter(year__year_value=year, month__month_number=month).exists():
                    year_month = cls.objects.get(
                        year__year_value=year,
                        month__month_number=month
                    )
                    month_data = {
                        "monthly_work_hour": year_month.monthly_work_hour,
                        "group_a_general_work_hour": year_month.group_a_general_work_hour,
                        "group_a_daytime_work_hour": year_month.group_a_daytime_work_hour,
                        "group_a_nighttime_work_hour": year_month.group_a_nighttime_work_hour,
                        "group_a_holiday_work_hour": year_month.group_a_holiday_work_hour,
                        "group_b_general_work_hour": year_month.group_b_general_work_hour,
                        "group_b_daytime_work_hour": year_month.group_b_daytime_work_hour,
                        "group_b_nighttime_work_hour": year_month.group_b_nighttime_work_hour,
                        "group_b_holiday_work_hour": year_month.group_b_holiday_work_hour,
                        "group_c_general_work_hour": year_month.group_c_general_work_hour,
                        "group_c_daytime_work_hour": year_month.group_c_daytime_work_hour,
                        "group_c_nighttime_work_hour": year_month.group_c_nighttime_work_hour,
                        "group_c_holiday_work_hour": year_month.group_c_holiday_work_hour,
                        "group_d_general_work_hour": year_month.group_d_general_work_hour,
                        "group_d_daytime_work_hour": year_month.group_d_daytime_work_hour,
                        "group_d_nighttime_work_hour": year_month.group_d_nighttime_work_hour,
                        "group_d_holiday_work_hour": year_month.group_d_holiday_work_hour,
                    }

                    year_data[month] = month_data

            work_calendar_data[year] = year_data

        return work_calendar_data

    def clean(self):
        if hasattr(self, "year") and hasattr(self, "month"):
            existing_entry = WorkCalendar.objects.filter(
                year=self.year,
                month=self.month
            ).exclude(pk=self.pk)

            if existing_entry.exists():
                raise ValidationError(
                    {
                        "month": _("Bu il və ay üçün məlumat artıq mövcuddur. Zəhmət olmasa fərqli bir il və ya ay seçin."),
                        "year": _("Bu il və ay üçün məlumat artıq mövcuddur. Zəhmət olmasa fərqli bir il və ya ay seçin."),
                    },
                )
        super().clean()
    
    class Meta:
        verbose_name = _("İş təqvimi")
        verbose_name_plural = _("İş təqvimləri")


class WorkCalendarImage(models.Model):
    year = models.ForeignKey(
        Year,
        on_delete=models.CASCADE,
        verbose_name=_("İl")
    )
    image = CustomImageField(
        verbose_name=_("Şəkil"),
        upload_to="work_calendar"
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
        return str(f"{self.year} - {self.image}")

    def clean(self):
        existing_image = WorkCalendarImage.objects.filter(
            year=self.year
        ).exclude(pk=self.pk)

        if existing_image.exists():
            raise ValidationError(
                {"year": _(
                    "Bu il üçün şəkil artıq mövcuddur. Zəhmət olmasa fərqli bir il seçin.")},
            )

    class Meta:
        verbose_name = _("İstehsalat təqvimi şəkili")
        verbose_name_plural = _("İstehsalat təqvimi şəkilləri")


class SalaryCalculation(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("İstifadəçi")
    )
    year = models.ForeignKey(
        Year,
        on_delete=models.PROTECT,
        verbose_name=_("İl")
    )
    month = models.ForeignKey(
        Month,
        on_delete=models.PROTECT,
        verbose_name=_("Ay")
    )
    shift = models.ForeignKey(
        Shift,
        on_delete=models.PROTECT,
        verbose_name=_("Növbə")
    )

    salary = models.DecimalField(
        verbose_name=_("Vəzifə maaşı"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    overtime = models.PositiveSmallIntegerField(
        verbose_name=_("Əlavə iş saatı"),
    )
    bonus_percent = models.PositiveSmallIntegerField(
        verbose_name=_("Mükafat faizi"),
        validators=[MaxValueValidator(500)]
    )
    hourly_wage = models.DecimalField(
        verbose_name=_("Saatlıq əməkhaqqı"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    night_work_pay = models.DecimalField(
        verbose_name=_("Gecə növbəsi ödənişi"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    extra_hour_pay = models.DecimalField(
        verbose_name=_("Növbədən artıq qalan saat ödənişi (ikiqat)"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    holiday_hour_pay = models.DecimalField(
        verbose_name=_("Bayram saatı ödənişi"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    overtime_pay = models.DecimalField(
        verbose_name=_("Əlavə iş saatı ödənişi (ikiqat)"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    bonus_pay = models.DecimalField(
        verbose_name=_("Mükafat məbləği"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    gross = models.DecimalField(
        verbose_name=_("Gross maaş"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    nett = models.DecimalField(
        verbose_name=_("Nett gəlir"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    income_tax = models.DecimalField(
        verbose_name=_("Gəlir vergisi"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    dsmf_tax = models.DecimalField(
        verbose_name=_("Məcburi dövlət sosial sığorta haqqı"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    unemployment_insurance_tax = models.DecimalField(
        verbose_name=_("İşsizlikdən sığorta haqqı"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    compulsory_health_insurance_tax = models.DecimalField(
        verbose_name=_("İcbari tibbi sığorta haqqı"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
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
        return str(f"{self.user} - {self.year} - {self.month} - {self.shift} - {self.nett}")

    class Meta:
        verbose_name = _("Maaş hesablaması")
        verbose_name_plural = _("Maaş hesablamaları")


class FAQ(models.Model):
    question = RichTextField(
        verbose_name=_("Sual"),
    )
    answer = RichTextField(
        verbose_name=_("Cavab")
    )
    display_order = models.PositiveSmallIntegerField(
        verbose_name=_("Göstərilmə sırası"),
        unique=True
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
        if len(strip_tags(self.question)) > 100:
            return f"{strip_tags(self.question)[:100]}..."
        else:
            return strip_tags(self.question)

    class Meta:
        verbose_name = _("Tez-tez verilən sual")
        verbose_name_plural = _("Tez-tez verilən suallar")


class Contact(models.Model):
    full_name = models.CharField(
        verbose_name=_("Ad Soyad"),
        max_length=100
    )
    email = models.EmailField(
        verbose_name=_("E-Poçt")
    )
    subject = models.CharField(
        verbose_name=_("Mövzu"),
        max_length=255
    )
    message = models.TextField(
        verbose_name=_("Mesaj")
    )
    is_resolved = models.BooleanField(
        verbose_name=_("Həll edildi"),
        default=False
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
        return f"{self.full_name} -- {self.subject}"

    class Meta:
        verbose_name = _("Əlaqə")
        verbose_name_plural = _("Əlaqələr")


class Subscriber(models.Model):
    email = models.EmailField(
        verbose_name=_("E-Poçt"),
        unique=True
    )
    subscription_status = models.BooleanField(
        verbose_name=_("Abunə statusu"),
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
        return self.email

    class Meta:
        verbose_name = _("Abunə")
        verbose_name_plural = _("Abunələr")


class SiteInfo(models.Model):
    name = models.CharField(
        verbose_name=_("Sayt adı"),
        max_length=50
    )
    logo = CustomImageField(
        verbose_name=_("Loqo"),
        upload_to="logo",
        blank=True,
        null=True
    )
    favicon = CustomImageField(
        verbose_name=_("Favicon"),
        upload_to="favicon",
        blank=True,
        null=True
    )
    privacy_policy_url = models.URLField(
        verbose_name=_("Gizlilik URL"),
        blank=True,
        null=True
    )
    terms_condition_url = models.URLField(
        verbose_name=_("Şərtlər & Qaydalar URL"),
        blank=True,
        null=True
    )
    facebook_url = models.URLField(
        verbose_name=_("Facebook URL"),
        blank=True,
        null=True
    )
    instagram_url = models.URLField(
        verbose_name=_("Instagram URL"),
        blank=True,
        null=True
    )
    youtube_url = models.URLField(
        verbose_name=_("Youtube URL"),
        blank=True,
        null=True
    )
    linkedin_url = models.URLField(
        verbose_name=_("Linkedin URL"),
        blank=True,
        null=True
    )
    github_url = models.URLField(
        verbose_name=_("Github URL"),
        blank=True,
        null=True
    )
    email1 = models.EmailField(
        verbose_name=_("Email 1"),
        blank=True,
        null=True
    )
    email2 = models.EmailField(
        verbose_name=_("Email 2"),
        blank=True,
        null=True
    )
    email3 = models.EmailField(
        verbose_name=_("Email 3"),
        blank=True,
        null=True
    )
    phone_number1 = models.CharField(
        verbose_name=_("Telefon nömrəsi 1"),
        max_length=40,
        blank=True,
        null=True
    )
    phone_number2 = models.CharField(
        verbose_name=_("Telefon nömrəsi 2"),
        max_length=40,
        blank=True,
        null=True
    )
    phone_number3 = models.CharField(
        verbose_name=_("Telefon nömrəsi 3"),
        max_length=40,
        blank=True,
        null=True
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
        return f"{self.name} #{self.id}"

    class Meta:
        verbose_name = _("Sayt məlumatı")
        verbose_name_plural = _("Sayt məlumatları")


class CalculationCount(models.Model):
    count = models.PositiveSmallIntegerField(
        verbose_name=_("Say"),
        default=0
    )
    created_at = models.DateTimeField(
        verbose_name=_("Yaradılma vaxtı"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Yenilənmə vaxtı"),
        auto_now=True
    )

    def save(self, *args, **kwargs):
        if CalculationCount.objects.exists() and not self.pk:
            raise ValidationError(_("Yalnızca bir ədəd obyekt yaratmağa icazə verilir"))
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.count}"

    class Meta:
        verbose_name = _("Hesablama sayı")
        verbose_name_plural = _("Hesablama sayı")


class AlertMessage(models.Model):
    class AlertType(models.TextChoices):
        INFO = "info", "Info"
        SUCCESS = "success", "Success"
        WARNING = "warning", "Warning"
        DANGER = "danger", "Danger"

    type = models.CharField(
        verbose_name=_("Tip"),
        max_length=10,
        choices=AlertType.choices,
        default=AlertType.INFO
    )
    text = models.CharField(
        verbose_name=_("Alert Mesajı"),
        max_length=255
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

    class Meta:
        verbose_name = _("Alert Mesajı")
        verbose_name_plural = _("Alert Mesajları")

    def __str__(self):
        return f"{self.get_type_display()}: {self.text}"