from django.core.management.base import BaseCommand
import pandas as pd
from core.models import Company


class Command(BaseCommand):
    help = 'Clears already populated Company data from the database'

    def handle(self, *args, **kwargs):

        companies = Company.objects.all()
        
        for company in companies:
            try:
                print(f'Deleting item {company.name}')
                company.delete()
            except Exception as err:
                print('Could not delete ', err)
        