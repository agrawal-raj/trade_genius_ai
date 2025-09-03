from django.db import models

# Create your models here.
class Company(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    company_logo = models.CharField(max_length=255, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    chart_link = models.CharField(max_length=255, blank=True, null=True)
    about_company = models.TextField(blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    nse_profile = models.CharField(max_length=255, blank=True, null=True)
    bse_profile = models.CharField(max_length=255, blank=True, null=True)
    face_value = models.IntegerField(blank=True, null=True)
    book_value = models.IntegerField(blank=True, null=True)
    roce_percentage = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    roe_percentage = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'companies'

class Analysis(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    company_id = models.CharField(max_length=50)
    compounded_sales_growth = models.CharField(max_length=50)
    compounded_profit_growth = models.CharField(max_length=50)
    stock_price_cagr  = models.CharField(max_length=50)
    roe = models.CharField(max_length=50)

    class Meta:
        db_table = 'analysis'

class ProsAndCons(models.Model):
    id = models.AutoField(primary_key=True)
    company_id = models.CharField(max_length=255)
    pros = models.CharField(max_length=255, blank=True, null=True)
    cons = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'prosandcons'
