# imagen de python
FROM python:3.10

#Ruta de trabajo
WORKDIR /app

# Copia los archivos al contenedor
COPY . .

# Instalacion de dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 9011
EXPOSE 9011

#Correr la app
CMD ["python", "potato-server.py"]