from django.contrib import admin

# Register your models here.

from multidb import MultiDBModelAdmin
from .models import Application
from omega.models import User, Cluster


class ApplicationAdmin(MultiDBModelAdmin):
    using = 'oapp'

    readonly_fields = ('id', 'name', 'uid', 'cid', 'instances',
                       'status', 'aliase', 'created', 'updated'
                      )

    list_display = ('id', 'name', 'get_user_email', 'get_cluster_name', 'instances', 'status', 'aliase', 'created', 'updated')
    search_fields = ['name']

    def get_user_email(self, obj):
        return User.objects.get(id=obj.uid).email
    get_user_email.admin_order_field = 'email'
    get_user_email.short_description = 'User Email'

    def get_cluster_name(self, obj):
        return Cluster.objects.get(id=obj.cid).name
    get_cluster_name.admin_order_field = 'cluster'
    get_cluster_name.short_description = 'Cluster Name'

admin.site.register(Application, ApplicationAdmin)
