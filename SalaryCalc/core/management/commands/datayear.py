from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Year

class Command(BaseCommand):
    help = 'Populate Year data'

    def handle(self, *args, **options):
        if not Year.objects.exists():
            data = [
                {'year_value': 2023},
                {'year_value': 2024}
            ]

            try:
                with transaction.atomic():
                    Year.objects.bulk_create([Year(**entry) for entry in data])
                self.stdout.write(self.style.SUCCESS('Year modeli melumatlari ugurla elave edildi.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Xeta bash verdi: {str(e)}'))
        else:
            self.stdout.write(self.style.WARNING('Melumat elave olunmadi!!! Melumat elave oluna bilmeyi uchun Year modeli bosh olmalidir.'))