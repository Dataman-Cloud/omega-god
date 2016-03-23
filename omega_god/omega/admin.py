from django import forms
from django.contrib import admin
from django.db import models

from multidb import MultiDBModelAdmin, MultiDBTabularInline
from daterange_filter.filter import DateTimeRangeFilter

from .models import User, Cluster, Node, Notice, Group


# Register your models here.

class ClusterInline(MultiDBTabularInline):
    using = 'omega'

    model = Cluster
    extra = 0
    readonly_fields = ('name', 'owner', 'cluster_type', 'master_ips',
                           'created_at', 'updated_at', 'status'
                      )


class NodeInline(MultiDBTabularInline):
    using = 'omega'

    model = Node
    extra = 0
    readonly_fields = ('id', 'name', 'ip', 'role', 'agent_version', 'created_at', 'updated_at')


class UserAdmin(MultiDBModelAdmin):
    using = 'omega'

    readonly_fields = ('id', 'email', 'company', 'wechat_qq',
                       'phone_number', 'invitation_code', 'last_login',
                        'created_at', 'updated_at', 'is_activated',
                        'is_superuser', 'is_stuff'
                      )
    fieldsets = [
        ('User Info', {'fields': ('id', 'email', 'company', 'wechat_qq', 'phone_number',
            'invitation_code', 'last_login', 'created_at',
            'updated_at')
            }
        ),
        ('Permissions', {'fields': ('is_activated',
            'is_superuser', 'is_stuff')
            }
        ),
    ]
    inlines = [ClusterInline]
    list_display = ('id', 'email', 'company', 'wechat_qq', 'phone_number', 'created_at', 'last_login', 'is_activated', 'is_superuser')
    list_filter = [('created_at', DateTimeRangeFilter), ('last_login', DateTimeRangeFilter), 'is_activated']
    search_fields = ['email', 'company', 'phone_number', 'wechat_qq']


class ClusterAdmin(MultiDBModelAdmin):
    using = 'omega'

    readonly_fields = ('name', 'owner', 'group', 'cluster_type', 'master_ips',
                       'created_at', 'updated_at', 'status'
                      )

    fieldsets = [
        ('Cluster Info', {'fields': ('name', 'owner', 'group',
            'cluster_type', 'master_ips', 'created_at',
            'updated_at')
            }
        ),
        ('Status', {'fields': ['status']
            }
        ),
    ]
    inlines = [NodeInline]
    list_display = ('id', 'name', 'cluster_type', 'status', 'created_at', 'get_user_email', 'get_user_company',
                    'get_group_name', 'get_nodes_count', 'get_created_at_of_the_last_node')
    list_filter = ['cluster_type', 'status', 'created_at']
    search_fields = ['name', 'owner__email', 'owner__company']

    def get_user_email(self, obj):
        return obj.owner.email
    get_user_email.admin_order_field = 'email'
    get_user_email.short_description = 'User Email'

    def get_user_company(self, obj):
        return obj.owner.company
    get_user_company.admin_order_field = 'company'
    get_user_company.short_description = 'User Company'

    def get_nodes_count(self, obj):
        return obj.nodes_count
    get_nodes_count.admin_order_field = 'nodes_count'
    get_nodes_count.short_description = 'Nodes Count'

    def get_created_at_of_the_last_node(self, obj):
        return obj.created_at_of_the_last_node
    get_created_at_of_the_last_node.admin_order_field = 'created_at_of_the_last_node'
    get_created_at_of_the_last_node.short_description = 'Last Node Created at'

    def get_group_name(self, obj):
        return obj.group.name
    get_group_name.admin_order_field = ''
    get_group_name.short_description = 'Group'


class NoticeAdmin(admin.ModelAdmin):
    using = 'omega'

    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = [
        ('Notice Info', {'fields': ('id', 'content', 'enabled', 'created_at')})
    ]
    list_display = ('id', 'content', 'enabled', 'created_at')
    list_filter = ['created_at', 'enabled']
    search_fields = ['created_at', 'enabled']

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(NoticeAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'content':
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield


class GroupAdmin(admin.ModelAdmin):
    using = 'omega'

    readonly_fields = ('id', 'name', 'owner', 'created_at', 'updated_at')
    fieldsets = [
        ('Group Info', {'fields': ('id', 'name', 'owner', 'created_at', 'updated_at')})
    ]
    list_display = ('id', 'name', 'get_user_email', 'get_member_count', 'created_at', 'updated_at')
    list_filter = [('created_at', DateTimeRangeFilter), ('updated_at', DateTimeRangeFilter)]
    search_fields = ['name', 'owner__email']

    def get_user_email(self, obj):
        return obj.owner.email
    get_user_email.admin_order_field = 'owner__email'
    get_user_email.short_description = 'Owner Email'

    def get_queryset(self, request):
        qs = super(GroupAdmin, self).get_queryset(request)
        qs = qs.annotate(models.Count('groupuser'))
        return qs

    def get_member_count(self, obj):
        return obj.groupuser__count
    get_member_count.admin_order_field = 'groupuser__count'
    get_member_count.short_description = 'Member Count'


admin.site.register(User, UserAdmin)
admin.site.register(Cluster, ClusterAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(Group, GroupAdmin)
