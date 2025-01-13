# Usa una imagen oficial de Python como base
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    gcc \
    && apt-get clean

# Copia el código de la aplicación al contenedor
COPY . .

# Instala las dependencias del proyecto
RUN pip install --no-cache-dir -r django-requirements.txt


# Define las variables de entorno necesarias para Django
# (puedes ajustar estas según tus necesidades)
ENV PYTHONUNBUFFERED=0
