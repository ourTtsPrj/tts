from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('stdcode', 'password', 'firstName', 'lastName', 'rank')}),
        ('Permissions', {'fields': (
            'is_superuser',
            'groups', 
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('stdcode', 'password1', 'password2','firstName','lastName','rank')
            }
        ),
    )

    list_display = ('stdcode', 'password', 'firstName', 'lastName', 'rank')
    list_filter = ('is_superuser','groups')
    search_fields = ('stdcode',)
    ordering = ('stdcode',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)