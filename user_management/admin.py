from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Esta es una forma más avanzada que usa la configuración por defecto
# pero la aplica a tu modelo CustomUser.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Puedes añadir campos extra aquí si tu CustomUser los tuviera
    # list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

admin.site.register(CustomUser, CustomUserAdmin)