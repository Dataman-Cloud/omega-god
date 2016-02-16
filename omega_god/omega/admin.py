from django import forms
from django.contrib import admin

from multidb import MultiDBModelAdmin, MultiDBTabularInline

from .models import User, Cluster, Node, Notice


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
    list_filter = ['created_at', 'last_login', 'is_activated']
    search_fields = ['email', 'company', 'phone_number', 'wechat_qq']


class ClusterAdmin(MultiDBModelAdmin):
    using = 'omega'

    readonly_fields = ('name', 'owner', 'cluster_type', 'master_ips',
                       'created_at', 'updated_at', 'status'
                      )

    fieldsets = [
        ('Cluster Info', {'fields': ('name', 'owner',
            'cluster_type', 'master_ips', 'created_at',
            'updated_at')
            }
        ),
        ('Status', {'fields': ['status']
            }
        ),
    ]
    inlines = [NodeInline]
    list_display = ('id', 'name', 'cluster_type', 'status', 'created_at', 'get_user_email', 'get_user_company', 'get_nodes_count', 'get_created_at_of_the_last_node')
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


class NoticeAdmin(admin.ModelAdmin):
    using = 'omega'

    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = [
        ('Notice Info', {'fields': ('id', 'content', 'created_at', 'updated_at')})
    ]
    list_display = ('id', 'content', 'created_at')
    list_filter = ['created_at']
    search_fields = ['created_at']

    # for markdown, webpage need show textarea
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(NoticeAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'content':
            formfield.widget = forms.Textarea(attrs=formfield.widget.attrs)
        return formfield


admin.site.register(User, UserAdmin)
admin.site.register(Cluster, ClusterAdmin)
admin.site.register(Notice, NoticeAdmin)
