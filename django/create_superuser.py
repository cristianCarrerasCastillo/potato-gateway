import os
import django
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestion_equipos.settings")
django.setup()

from django.contrib.auth.models import User

# Datos del superusuario desde variables de entorno
username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin")

# Crear el superusuario solo si no existe
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superusuario '{username}' creado exitosamente.")
else:
    print(f"Superusuario '{username}' ya existe.")
