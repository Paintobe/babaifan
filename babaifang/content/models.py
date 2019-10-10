from django.db import models

# Create your models here.
class LunBoTu(models.Model):
    img = models.CharField(max_length=50)
    title = models.CharField(max_length=20)
    backColor = models.CharField(max_length=20)

    class Meta:
        db_table = 'tblunbotu'


class ReMaiTu(models.Model):
    mane = models.CharField(max_length=50)
    tits = models.CharField(max_length=50)
    price1 = models.DecimalField(max_digits=6,decimal_places=2)
    price2 = models.DecimalField(max_digits=6,decimal_places=2)
    img = models.CharField(max_length=50)

    class Meta:
        db_table = 'tbremaitu'