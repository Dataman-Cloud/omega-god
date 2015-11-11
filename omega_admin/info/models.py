import datetime
import uuid

from django.db import models
from django.utils import timezone

# Create your models here.

class Base(models.Model):

    class Meta:
       abstract = True
       app_label = 'info'
    
    created_at = models.DateTimeField(default=timezone.now, null=True) 
    updated_at = models.DateTimeField(default=timezone.now, null=True) 

class User(Base):

    class Meta:
       db_table = 'user'
       app_label = 'info'

    id = models.AutoField(primary_key=True) 
    email = models.EmailField(max_length=128, unique=True, null=False)
    invitation_code = models.CharField(max_length=128, null=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True)     #
    password = models.BinaryField(max_length=1024, null=False)     #
    is_superuser = models.BooleanField(null=False) 
    is_stuff = models.BooleanField(null=False) 
    last_login = models.DateTimeField(default=timezone.now, null=True) 
    is_activated = models.BooleanField(default=False) 

    def __str__(self):
        return self.email

class Cluster(Base):

    class Meta:
       db_table = 'cluster'
       app_label = 'info'

    TYPES = [
        ("1_master", "1_master"),
        ("3_masters", "3_masters"),
        ("5_masters", "5_masters")
    ]

    STATUS = [
        ("uninstalled", "uninstalled"),
        ("running", "running"),
        ("installing", "installing"),
        ("failed", "failed")
    ]

    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=200, null=False)
    cluster_type = models.CharField(max_length=255, choices=TYPES, default='1_master')
    status = models.CharField(max_length=255, choices=STATUS, default='uninstalled', null=False)
    master_ips = models.CharField(max_length=255)
    owner = models.ForeignKey(User)

    def __str__(self):
        return self.name

class Node(Base):

    class Meta:
       db_table = 'node'
       app_label = 'info'

    STATUSES = [
        ('pending', 'pending'),
        ('installing', 'installing'),
        ('running', 'running'),
        ('terminating', 'terminating'),
        ('terminated', 'terminated'),
    ]
    ROLES = [
        ('master', 'master'),
        ('slave', 'slave')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, null=True)
    cluster = models.ForeignKey(Cluster) 
    status = models.CharField(max_length=255, choices=STATUSES, null=False)
    ip = models.GenericIPAddressField(null=True)
    role = models.CharField(max_length=255, choices=ROLES, null=True)

    def __str__(self):
        return self.name

class NodeAttribute(Base):

    class Meta:
       db_table = 'node_attribute'
       app_label = 'info'

    ATTRIBUTES = [
        ('transient', 'transient'),
        ('gateway', 'gateway'),
        ('proxy', 'proxy'),
        ('persistent', 'persistent')
    ]

    id = models.AutoField(primary_key=True) 
    node = models.ForeignKey(Node) 
    attribute = models.CharField(max_length=255, choices=ATTRIBUTES, null=False, default='transient')
    
class Service(Base):

    class Meta:
       db_table = 'service'
       app_label = 'info'

    ISOLATORS = [
        ('bare', 'bare'),
        ('container', 'container'),
    ]
    STATUSES = [
        ('installing', 'installing'),
        ('failed', 'failed'),
        ('running', 'running'),
        ('uninstalling', 'uninstalling'),
        ('uninstalled', 'uninstalled'),
    ]
    NAMES = [
        ('master', 'master'),
        ('slave', 'slave'),
        ('zookeeper', 'zookeeper'),
        ('marathon', 'marathon'),
        ('logcollection', 'logcollection'),
        ('cadvisor', 'cadvisor'),
        ('exhibitor', 'exhibitor')
    ]

    id = models.AutoField(primary_key=True) 
    name  = models.CharField(max_length=255, choices=NAMES, null=False, default='master')
    node = models.ForeignKey(Node)
    isolator  = models.CharField(max_length=255, choices=ISOLATORS, null=False, default='container')
    status  = models.CharField(max_length=255, choices=STATUSES, null=False, default='uninstalled')
    
