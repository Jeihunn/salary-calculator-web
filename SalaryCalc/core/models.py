from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


# Create your models here.


class AbstractModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name=_("Yaradılma vaxtı"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("Yenilənmə vaxtı"),
        auto_now=True
    )

    class Meta:
        abstract = True


class Year(AbstractModel):
    year_value = models.PositiveSmallIntegerField(
        verbose_name=_("İl"),
        unique=True
    )

    def __str__(self):
        return str(self.year_value)

    class Meta:
        verbose_name = _("İl")
        verbose_name_plural = _("İllər")


class Month(AbstractModel):
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

    def __str__(self):
        return f"{self.name} ({self.month_number})"

    class Meta:
        verbose_name = _("Ay")
        verbose_name_plural = _("Aylar")


class WorkCalendar(AbstractModel):
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
        null=True,
        blank=True,
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
        null=True,
        blank=True,
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
        null=True,
        blank=True,
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
        null=True,
        blank=True,
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
        verbose_name = _("İş Təqvimi")
        verbose_name_plural = _("İş Təqvimləri")


class WorkCalendarImage(AbstractModel):
    year = models.ForeignKey(
        Year,
        on_delete=models.CASCADE,
        verbose_name=_("İl")
    )
    image = models.ImageField(
        verbose_name=_("Şəkil"),
        upload_to="work_calendar"
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
        verbose_name = _("İstehsalat Təqvimi Şəkili")
        verbose_name_plural = _("İstehsalat Təqvimi Şəkilləri")
