import csv

from django.core.management.base import BaseCommand


from sales.models import coral_sale
from django.contrib.auth.models import User
class Command(BaseCommand):
    help = 'Import bite exercise stats'

    def add_arguments(self, parser):
        parser.add_argument('-c', '--csv', required=True)
        parser.add_argument('-u', '--user', required=True)
    def handle(self, *args, **options):
        file = options["csv"]
        user = options["user"]
        with open(file) as f:
            reader = csv.DictReader(f)
            for row in reader:

                for number in  range(int(row["Quanity"])):
                    print(row)
                    coral_sale.objects.create(coral_name=row["Type"],sale_date=row["Date"],sale_price=row["Price"],species=row["Species"],user_id=user)