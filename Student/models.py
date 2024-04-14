# models.py
from django.db import models

class Job(models.Model):
    Company_ID = models.CharField(max_length=10)
    Company_Name = models.CharField(max_length=255)
    Domain = models.CharField(max_length=25)
    Job_Description = models.CharField(max_length=255)
    Min_Salary = models.DecimalField(max_digits=10, decimal_places=2)
    Max_Salary = models.DecimalField(max_digits=10, decimal_places=2)
    Job_Type = models.CharField(max_length=20)
    Location = models.CharField(max_length=25)
    Eligibility_Criteria = models.DecimalField(max_digits=5, decimal_places=2)
    Email_Address = models.CharField(max_length=25)
    Phone = models.CharField(max_length=10)

    def __str__(self):
        return(f"{self.company_name}")
