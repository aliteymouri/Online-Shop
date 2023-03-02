from accounts.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib import admin
from accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'is_admin', 'phone_number')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'phone_number', 'email', 'melli_code', 'avatar', 'password',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'phone_number', 'email', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'phone_number')
    ordering = ('username',)
    filter_horizontal = ()

    def has_add_permission(self, req):
        if req.user.is_admin:
            return True
        return False

    def has_change_permission(self, req, obj=None):
        if req.user.is_admin:
            return True
        return False

    def has_delete_permission(self, req, obj=None):
        if req.user.is_admin:
            return True
        return False


admin.site.unregister(Group)
