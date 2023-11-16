from django.db import models
from django.contrib.auth.models import User

class Member(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)

  def __str__(self):
    return f"{self.firstname} {self.lastname}"

class Data(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # lub domyślnie przypisane do pewnej wartości
  SN = models.CharField(max_length=255, default=0)
  Time = models.DateTimeField()
  date = models.DateField(blank=True, null=True)
  time_of_day = models.TimeField(blank=True, null=True)
  Vpv1 = models.FloatField(default=0)
  Vpv2 = models.FloatField(default=0)
  Ipv1 = models.FloatField(default=0)
  Ipv2 = models.FloatField(default=0)
  Vac1 = models.FloatField(default=0)
  Vac2 = models.FloatField(default=0)
  Vac3 = models.FloatField(default=0)
  Iac1 = models.FloatField(default=0)
  Iac2 = models.FloatField(default=0)
  Iac3 = models.FloatField(default=0)
  Pac = models.IntegerField(default=0)
  Fac = models.FloatField(default=0)
  E_Total = models.FloatField(default=0)
  H_Total = models.IntegerField(default=0)
  E_Today = models.FloatField(default=0)
  Temp = models.FloatField(default=0)

  def __str__(self):
    return f"{self.Time}"