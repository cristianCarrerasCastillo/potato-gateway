from django.db import models

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    mac = models.CharField(max_length=100, unique=True)
    hardware = models.CharField(max_length=100, blank=True, null=True)
    creado_en = models.DateField(auto_created=True)
    located = models.CharField(max_length=200)
    stated = models.SmallIntegerField()

    def __str__(self):
        return self.name