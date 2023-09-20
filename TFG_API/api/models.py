from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reference = models.CharField(primary_key=True, max_length=50, null=False, blank=False, unique=True, error_messages={'unique':"Ya existe un proyecto con esa referencia"})
    year = models.PositiveIntegerField(validators=[MaxValueValidator(2023), MinValueValidator(2000)], default=2023, null=False, blank=False)
    convocatory = models.CharField(max_length=400, null=False, blank=False)
    area = models.CharField(max_length=100, null=False, blank=False)
    subarea = models.CharField(max_length=100, null=False, blank=False)
    title = models.CharField(max_length=400, null=False, blank=False)
    cif = models.CharField(max_length=100, null=False, blank=False)
    ccaa = models.CharField(max_length=100, null=False, blank=False)
    city = models.CharField(max_length=50, null=False, blank=False)
    money = models.PositiveIntegerField(default=0, null=False, blank=False)


class Publication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    idScopus = models.CharField(primary_key=True, max_length=100, null=False, blank=False)
    creator = models.CharField(max_length=50, null=False, blank=False)
    authors = models.CharField(max_length=2000, null=False, blank=False)
    title = models.CharField(max_length=400, null=False, blank=False)
    year = models.PositiveIntegerField(validators=[MaxValueValidator(2000), MinValueValidator(2023)])
    source = models.CharField(max_length=100, null=False, blank=False)
    volume = models.CharField(max_length=100, null=True, blank=False)
    issue = models.PositiveIntegerField(null=True, blank=False)
    start = models.PositiveIntegerField(null=True, blank=True)
    end = models.PositiveIntegerField(null=True, blank=True)
    doi = models.CharField(max_length=100, null=True, blank=False)
    cited = models.PositiveIntegerField(default=0, null=False, blank=False)
    RAW = models.TextField(null=False, blank=False)
