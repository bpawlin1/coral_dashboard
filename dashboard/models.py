from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class apexMeasurments(models.Model):
    temp = models.DecimalField(max_digits=4, decimal_places=2)
    ph = models.DecimalField(max_digits=4, decimal_places=2)
    alk = models.DecimalField(max_digits=4, decimal_places=2) 
    calc = models.IntegerField()
    mag = models.IntegerField()
    date_created = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)