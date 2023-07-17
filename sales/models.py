from django.db import models
from coral.models import Coral
from django.contrib.auth.models import User
from datetime import date

class coral_sale(models.Model):
    coral_name = models.ForeignKey(Coral, on_delete=models.PROTECT)  # 0 to 32767
    sale_price = models.DecimalField(max_digits=6, decimal_places=2)  # I don't care about time here
    sale_date = models.DateField()
    species = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

