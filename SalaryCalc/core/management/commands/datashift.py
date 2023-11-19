from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Shift

class Command(BaseCommand):
    help = 'Populate Shift data'

    def handle(self, *args, **options):
        if not Shift.objects.exists():
            data = [
                {'name': 'A', 'value': 'a'},
                {'name': 'B', 'value': 'b'},
                {'name': 'C', 'value': 'c'},
                {'name': 'D', 'value': 'd'},
                {'name': 'Gündəlik', 'value': 'g'}
            ]

            try:
                with transaction.atomic():
                    Shift.objects.bulk_create([Shift(**entry) for entry in data])
                self.stdout.write(self.style.SUCCESS('Shift modeli məlumatları uğurla əlavə edildi.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Xəta baş verdi: {str(e)}'))
        else:
            self.stdout.write(self.style.WARNING('Məlumat əlavə olunmadı!!! Məlumat əlavə oluna bilməyi üçün Shift modeli boş olmalıdır.'))
        