from django.contrib import admin

from .models import User, Cluster, Node
# Register your models here.

class MultiDBModelAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = 'omega'
    actions = None

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(MultiDBModelAdmin, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_foreignkey(db_field, request=request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(MultiDBModelAdmin, self).formfield_for_manytomany(db_field, request=request, using=self.using, **kwargs)

class MultiDBTabularInline(admin.TabularInline):
    using = 'omega'

    def get_queryset(self, request):
        # Tell Django to look for inline objects on the 'other' database.
        return super(MultiDBTabularInline, self).get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'other' database.
        return super(MultiDBTabularInline, self).formfield_for_foreignkey(db_field, request=request, using=self.using, **kwargs)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        return super(MultiDBTabularInline, self).formfield_for_manytomany(db_field, request=request, using=self.using, **kwargs)

class ClusterInline(MultiDBTabularInline):
    model = Cluster
    extra = 0

class NodeInline(MultiDBTabularInline):
    model = Node
    extra = 0

class UserAdmin(MultiDBModelAdmin):
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
    

class ClusterAdmin(MultiDBModelAdmin):
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

