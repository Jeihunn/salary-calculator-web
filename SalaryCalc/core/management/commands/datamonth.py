from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Month

class Command(BaseCommand):
    help = 'Populate Month data'

    def handle(self, *args, **options):
        if not Month.objects.exists():
            data = [
                {'name': 'Yanvar', 'month_number': 1},
                {'name': 'Fevral', 'month_number': 2},
                {'name': 'Mart', 'month_number': 3},
                {'name': 'Aprel', 'month_number': 4},
                {'name': 'May', 'month_number': 5},
                {'name': 'İyun', 'month_number': 6},
                {'name': 'İyul', 'month_number': 7},
                {'name': 'Avqust', 'month_number': 8},
                {'name': 'Sentyabr', 'month_number': 9},
                {'name': 'Oktyabr', 'month_number': 10},
                {'name': 'Noyabr', 'month_number': 11},
                {'name': 'Dekabr', 'month_number': 12}
            ]

            try:
                with transaction.atomic():
                    Month.objects.bulk_create([Month(**entry) for entry in data])
                self.stdout.write(self.style.SUCCESS('Month modeli məlumatları uğurla əlavə edildi.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Xəta baş verdi: {str(e)}'))
        else:
            self.stdout.write(self.style.WARNING('Məlumat əlavə olunmadı!!! Məlumat əlavə oluna bilməyi üçün Month modeli boş olmalıdır.'))