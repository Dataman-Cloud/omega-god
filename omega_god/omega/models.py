import datetime
import uuid

from django.db import models
from django.utils import timezone

# Create your models here.

class Base(models.Model):

    class Meta:
       abstract = True
       app_label = 'omega'

    created_at = models.DateTimeField(default=timezone.now, null=True)
    updated_at = models.DateTimeField(default=timezone.now, null=True)

class User(Base):

    class Meta:
       db_table = 'user'
       app_label = 'omega'

    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=128, unique=True, null=False)
    invitation_code = models.CharField(max_length=128, null=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True)     #
    password = models.BinaryField(max_length=1024, null=False)     #
    is_superuser = models.BooleanField(null=False)
    is_stuff = models.BooleanField(null=False)
    last_login = models.DateTimeField(default=timezone.now, null=True)
    is_activated = models.BooleanField(default=False)
    company = models.CharField(max_length=128, null=False)
    wechat_qq = models.CharField(max_length=128, null=False)

    def __str__(self):
        return self.email

class Cluster(Base):

    class Meta:
       db_table = 'cluster'
       app_label = 'omega'

    id = models.AutoField(primary_key=True)
    @property
    def nodes_count(self):
        return Node.objects.filter(cluster__id=self.id).count()

    @property
    def created_at_of_the_last_node(self):
        try:
            return Node.objects.filter(cluster__id=self.id).order_by('-created_at')[0].created_at
        except:
            return "None"

    name = models.CharField(max_length=200, null=False)
    cluster_type = models.CharField(max_length=255, default='1_master')
    status = models.CharField(max_length=255, default='uninstalled', null=False)
    master_ips = models.CharField(max_length=255)
    owner = models.ForeignKey(User)

    def __str__(self):
        return self.name

class Node(Base):

    class Meta:
       db_table = 'node'
       app_label = 'omega'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, null=True)
    cluster = models.ForeignKey(Cluster)
    ip = models.GenericIPAddressField(null=True)
    role = models.CharField(max_length=255, null=True)
    agent_version = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

class NodeAttribute(Base):

    class Meta:
       db_table = 'node_attribute'
       app_label = 'omega'

    id = models.AutoField(primary_key=True)
    node = models.ForeignKey(Node)
    attribute = models.CharField(max_length=255, null=False)

class Service(Base):

    class Meta:
       db_table = 'service'
       app_label = 'omega'

    id = models.AutoField(primary_key=True)
    name  = models.CharField(max_length=255, null=False, default='master')
    node = models.ForeignKey(Node)
    isolator  = models.CharField(max_length=255, null=False, default='container')
    status  = models.CharField(max_length=255, null=False, default='uninstalled')
    version = models.CharField(max_length=255, null=False)


class Notice(Base):

    class Meta:
        db_table = 'notice'
        app_label = 'omega'

    id = models.AutoField(primary_key=True)
    content = models.CharField(max_length=1000, null=True)
    enabled = models.BooleanField(default=False, null=False)
