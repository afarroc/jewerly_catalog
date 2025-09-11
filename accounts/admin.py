from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User
import logging

logger = logging.getLogger(__name__)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for the User model
    """
    # Campos que se muestran en la lista de usuarios
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'phone_number',
        'is_customer',
        'is_staff',
        'is_active',
        'date_joined',
        'last_login'
    )

    # Campos por los que se puede filtrar
    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
        'is_customer',
        'date_joined',
        'last_login',
        ('groups', admin.RelatedOnlyFieldListFilter),
    )

    # Campos de búsqueda
    search_fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'phone_number'
    )

    # Campos de solo lectura
    readonly_fields = (
        'date_joined',
        'last_login',
        'user_permissions_list'
    )

    # Ordenamiento por defecto
    ordering = ('-date_joined',)

    # Configuración de los campos en el formulario de edición
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        (_('Personal info'), {
            'fields': (
                'first_name',
                'last_name',
                'email',
                'phone_number',
                'address',
                'billing_address'
            )
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'is_customer',
                'groups',
                'user_permissions'
            )
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )

    # Configuración de los campos al agregar un nuevo usuario
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'phone_number',
                'password1',
                'password2',
                'is_staff',
                'is_superuser',
                'is_customer',
                'is_active'
            ),
        }),
    )

    # Acciones personalizadas
    actions = [
        'activate_users',
        'deactivate_users',
        'make_staff',
        'remove_staff',
        'make_customer',
        'remove_customer'
    ]

    def user_permissions_list(self, obj):
        """Mostrar lista de permisos del usuario"""
        return ", ".join([p.name for p in obj.user_permissions.all()])
    user_permissions_list.short_description = _('User Permissions')

    def activate_users(self, request, queryset):
        """Activar usuarios seleccionados"""
        updated = queryset.update(is_active=True)
        self.message_user(
            request,
            ngettext(
                '%d user was successfully activated.',
                '%d users were successfully activated.',
                updated,
            ) % updated,
        )
        logger.info(f"Activated {updated} users by {request.user.username}")
    activate_users.short_description = _("Activate selected users")

    def deactivate_users(self, request, queryset):
        """Desactivar usuarios seleccionados"""
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            ngettext(
                '%d user was successfully deactivated.',
                '%d users were successfully deactivated.',
                updated,
            ) % updated,
        )
        logger.info(f"Deactivated {updated} users by {request.user.username}")
    deactivate_users.short_description = _("Deactivate selected users")

    def make_staff(self, request, queryset):
        """Convertir usuarios seleccionados en staff"""
        updated = queryset.update(is_staff=True)
        self.message_user(
            request,
            ngettext(
                '%d user was successfully made staff.',
                '%d users were successfully made staff.',
                updated,
            ) % updated,
        )
        logger.info(f"Made {updated} users staff by {request.user.username}")
    make_staff.short_description = _("Make selected users staff")

    def remove_staff(self, request, queryset):
        """Remover permisos de staff a usuarios seleccionados"""
        updated = queryset.update(is_staff=False)
        self.message_user(
            request,
            ngettext(
                '%d user staff status was successfully removed.',
                '%d users staff status were successfully removed.',
                updated,
            ) % updated,
        )
        logger.info(f"Removed staff status from {updated} users by {request.user.username}")
    remove_staff.short_description = _("Remove staff status from selected users")

    def make_customer(self, request, queryset):
        """Marcar usuarios seleccionados como clientes"""
        updated = queryset.update(is_customer=True)
        self.message_user(
            request,
            ngettext(
                '%d user was successfully marked as customer.',
                '%d users were successfully marked as customer.',
                updated,
            ) % updated,
        )
        logger.info(f"Marked {updated} users as customers by {request.user.username}")
    make_customer.short_description = _("Mark selected users as customers")

    def remove_customer(self, request, queryset):
        """Remover marca de cliente a usuarios seleccionados"""
        updated = queryset.update(is_customer=False)
        self.message_user(
            request,
            ngettext(
                '%d user customer status was successfully removed.',
                '%d users customer status were successfully removed.',
                updated,
            ) % updated,
        )
        logger.info(f"Removed customer status from {updated} users by {request.user.username}")
    remove_customer.short_description = _("Remove customer status from selected users")

    def get_queryset(self, request):
        """Optimizar consultas para incluir campos relacionados"""
        return super().get_queryset(request).select_related()

    def save_model(self, request, obj, form, change):
        """Log cuando se guarda un usuario"""
        action = "updated" if change else "created"
        super().save_model(request, obj, form, change)
        logger.info(f"User {obj.username} was {action} by {request.user.username}")

    def delete_model(self, request, obj):
        """Log cuando se elimina un usuario"""
        logger.info(f"User {obj.username} was deleted by {request.user.username}")
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        """Log cuando se eliminan múltiples usuarios"""
        count = queryset.count()
        usernames = list(queryset.values_list('username', flat=True))
        logger.info(f"Users {usernames} were deleted by {request.user.username}")
        super().delete_queryset(request, queryset)
