from django.core.management.base import BaseCommand
import pandas as pd
from core.models import Company


class Command(BaseCommand):
    help = "Populates Companies Database from csv file"

    def handle(self, *args, **kwargs):

        df = pd.read_csv("data/companies.csv")

        result = df.head(10)

        for index, row in df.iloc[501:].iterrows():
            try:
                current_item = Company(
                    name=row.get("name"),
                    rating=row.get("rating"),
                    review=row.get("review"),
                    company_type=row.get("company_type"),
                    head_quarters=row.get("Head_Quarters"),
                    company_age=row.get("Company_Age"),
                    no_of_employee=row.get("No_of_Employee"),
                )

                current_item.save()
                print("Data saved for ", current_item.name)
            except Exception as err:
                print("Could not save data for this item ", err)
