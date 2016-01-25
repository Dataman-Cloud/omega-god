import datetime

from django.db import models

from django.db import models
from django.utils import timezone
# Create your models here.

class Base(models.Model):

    class Meta:
       abstract = True
       app_label = 'oapp'

    created = models.DateTimeField(default=timezone.now, null=True)
    updated = models.DateTimeField(default=timezone.now, null=True)

class Application(Base):

    class Meta:
       db_table = 'application'
       app_label = 'oapp'

    id = models.AutoField(primary_key=True)
    uid = models.CharField(max_length=64, null=True)
    cid = models.CharField(max_length=64, null=True)
    name = models.CharField(max_length=64, null=True)
    instances = models.BigIntegerField(null=True)
    status = models.IntegerField(null=True)
    aliase = models.CharField(max_length=64, null=True)

    def __str__(self):
        return self.name
