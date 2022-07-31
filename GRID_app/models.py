from django.db import models

# Create your models here.
class Employees(models.Model):
    employeenumber = models.IntegerField(db_column='employeeNumber', primary_key=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=50)  # Field name made lowercase.
    firstname = models.CharField(db_column='firstName', max_length=50)  # Field name made lowercase.
    extension = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    jobtitle = models.CharField(db_column='jobTitle', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'employees'