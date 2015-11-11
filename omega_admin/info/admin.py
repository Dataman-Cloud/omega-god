from django.contrib import admin

# Register your models here.

from .models import User, Cluster, Node

class ClusterInline(admin.TabularInline):
    model = Cluster
    extra = 0

class NodeInline(admin.TabularInline):
    model = Node
    extra = 0

class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User Info', {'fields': ('email', 'phone_number',
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
    list_display = ('id', 'email', 'phone_number', 'invitation_code', 'created_at', 'last_login', 'is_activated', 'is_superuser')
    list_filter = ['last_login']
    search_fields = ['email']
    

class ClusterAdmin(admin.ModelAdmin):
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
    list_display = ('id', 'name', 'owner', 'cluster_type', 'master_ips', 'status', 'created_at', 'updated_at')
    list_filter = ['cluster_type', 'owner']
    search_fields = ['name']

admin.site.register(User, UserAdmin)
admin.site.register(Cluster, ClusterAdmin)

