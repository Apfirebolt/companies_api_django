from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    rating = models.FloatField()
    review = models.TextField()
    company_type = models.CharField(max_length=50, null=True, blank=True)
    head_quarters = models.CharField(max_length=100, null=True, blank=True)
    company_age = models.CharField(max_length=250, null=True, blank=True)
    no_of_employee = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name
