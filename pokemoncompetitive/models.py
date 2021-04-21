from django.db import models

# Create your models here.
class Mon_Names(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Pokemon:
        db_table = 'mon_names'
