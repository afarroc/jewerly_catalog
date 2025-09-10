#!/usr/bin/env python
"""
Script para crear superusuario administrador
Ejecutar: python create_superuser.py
"""
import os
import sys
import django
from getpass import getpass

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jewerly_catalog.settings')
django.setup()

from accounts.models import User

def create_superuser():
    print("=== CREANDO SUPERUSUARIO ADMINISTRADOR ===")

    # Datos del administrador
    admin_data = {
        'username': 'admin',
        'email': 'admin@tudominio.com',
        'first_name': 'Administrador',
        'last_name': 'Sistema'
    }

    # Verificar si ya existe
    existing_user = User.objects.filter(username=admin_data['username']).first()
    if existing_user:
        if existing_user.is_superuser:
            print(f"AVISO: El superusuario '{admin_data['username']}' ya existe.")
            print(f"Email: {existing_user.email}")
            print(f"Es superusuario: {existing_user.is_superuser}")
            return
        else:
            print(f"AVISO: El usuario '{admin_data['username']}' existe pero no es superusuario.")
            print("Convirtiendolo en superusuario...")
            existing_user.is_superuser = True
            existing_user.is_staff = True
            existing_user.save()
            print("EXITO: Usuario convertido en superusuario!")
            return

    # Solicitar contraseña
    print("Ingresa la contraseña para el administrador:")
    password = getpass("Contrasena: ")
    password_confirm = getpass("Confirmar contrasena: ")

    # Validaciones
    if password != password_confirm:
        print("ERROR: Las contrasenas no coinciden.")
        return

    if len(password) < 8:
        print("ERROR: La contrasena debe tener al menos 8 caracteres.")
        return

    # Crear superusuario
    try:
        admin_user = User.objects.create_superuser(
            username=admin_data['username'],
            email=admin_data['email'],
            password=password,
            first_name=admin_data['first_name'],
            last_name=admin_data['last_name']
        )

        print("\nEXITO: Superusuario creado exitosamente!")
        print(f"Username: {admin_user.username}")
        print(f"Email: {admin_user.email}")
        print(f"Nombre: {admin_user.get_full_name()}")
        print(f"Es superusuario: {admin_user.is_superuser}")
        print(f"Es staff: {admin_user.is_staff}")

        print("\n=== ACCESO AL PANEL DE ADMINISTRACION ===")
        print("URL Local: http://localhost:8000/admin")
        print("URL Produccion: https://tu-app.onrender.com/admin")
        print(f"Usuario: {admin_data['username']}")
        print(f"Email: {admin_data['email']}")
        print("Contrasena: [La que configuraste]")

        print("\n=== PERMISOS DEL ADMINISTRADOR ===")
        print("- Gestionar productos y categorias")
        print("- Ver y gestionar pedidos")
        print("- Administrar usuarios")
        print("- Configurar sitio web")
        print("- Ver reportes y estadisticas")

        print("\n=== IMPORTANTE ===")
        print("- CAMBIA la contrasena despues del primer login")
        print("- Mantén estas credenciales seguras")
        print("- No uses este usuario para compras normales")
        print("- Comparte solo con personal autorizado")

    except Exception as e:
        print(f"ERROR al crear el superusuario: {e}")

if __name__ == '__main__':
    create_superuser()