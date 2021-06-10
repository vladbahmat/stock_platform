from django.db import models

class Currency(models.Model):
    code = models.CharField("Code", max_length=5, unique=True)
    name = models.CharField("Name", max_length=15, unique=True, null=True)

    def __str__(self):
        return self.code