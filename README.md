# Smart Plant Server

Este proyecto es un sistema completo para monitorear y registrar la humedad del suelo desde dispositivos IoT, almacenar los datos en una base de datos MySQL, y visualizarlos mediante Grafana. Está diseñado para ejecutarse en contenedores Docker, facilitando su despliegue y mantenimiento.

## Características

- **Recepción de datos IoT**: Un servidor Python basado en `asyncio` para recibir datos (MAC y humedad) desde dispositivos IoT.
- **Almacenamiento de datos**: Base de datos MySQL para registrar las mediciones con soporte para múltiples equipos.
- **Visualización de datos**: Integración con Grafana para gráficos en tiempo real y análisis histórico.
- **Infraestructura Docker**: Contenedores Docker para el servidor, base de datos, y sistema de visualización.

---

## Requisitos

- [Docker](https://www.docker.com/) y [Docker Compose](https://docs.docker.com/compose/) instalados.
- Opcional: Cliente `netcat` para probar el servidor IoT localmente.

---

## Configuración Inicial

1. **Clonar el repositorio:**
   ```bash
   git clone <URL del repositorio>
   cd <nombre del repositorio>
   ```

2. **Estructura de directorios:**
   Asegúrate de tener los siguientes directorios y archivos:
   ```
   /db/init.sql         # Script para inicializar la base de datos
   /server/potato-server.py # Código del servidor IoT
   /django/             # Aplicación Django (opcional)
   docker-compose.yml   # Configuración de Docker Compose
   ```

3. **Variables de entorno:**
   Crea archivos `.env` en las carpetas necesarias para configurar las credenciales:

   - `db/.env`:
     ```env
     MYSQL_ROOT_PASSWORD=rootpassword
     MYSQL_DATABASE=plantStatus
     MYSQL_USER=user
     MYSQL_PASSWORD=password
     ```

   - `django/.env`:
     ```env
     DJANGO_SUPERUSER_USERNAME=admin
     DJANGO_SUPERUSER_EMAIL=admin@example.com
     DJANGO_SUPERUSER_PASSWORD=admin
     ```

---

## Instrucciones de Uso

### 1. **Levantar los contenedores:**
   Ejecuta el siguiente comando para inicializar los contenedores:
   ```bash
   docker-compose up --build
   ```

   Esto iniciará:
   - Base de datos MySQL
   - Servidor Python (`potato-server.py`)
   - Grafana

### 2. **Probar el servidor IoT:**
   Envía datos simulados al servidor usando `netcat`:
   ```bash
   echo "12:34:56:78:9A:BC,45" | nc localhost 9011
   ```

   El servidor registrará estos datos en la tabla `plantSense`.

### 3. **Acceso a Grafana:**
   - URL: [http://localhost:3000](http://localhost:3000)
   - Usuario: `admin`
   - Contraseña: `admin` (o la configurada en `docker-compose.yml`)

   Agrega la base de datos MySQL como fuente de datos y crea dashboards para visualizar las mediciones de humedad.

---

## Estructura de la Base de Datos

### Tabla `equiment`:
Registra los dispositivos IoT.

```sql
CREATE TABLE equiment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    mac VARCHAR(100) UNIQUE NOT NULL,
    hardware VARCHAR(100),
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    located VARCHAR(200) NOT NULL,
    stated SMALLINT NOT NULL
);
```

### Tabla `plantSense`:
Registra las mediciones de humedad enviadas por los dispositivos.

```sql
CREATE TABLE plantSense (
    id INT AUTO_INCREMENT PRIMARY KEY,
    equiment_id INT,
    mac VARCHAR(100) NOT NULL,
    humedity DECIMAL(5,2) NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (equiment_id) REFERENCES equiment(id) ON DELETE CASCADE
);
```

---

## Solución de Problemas

- **La base de datos no tiene las tablas:**
  Asegúrate de que el script `init.sql` esté en `/db` y vuelva a iniciar los contenedores con:
  ```bash
  docker-compose down
  docker-compose up --build
  ```

- **El servidor IoT no responde:**
  Verifica los logs del contenedor:
  ```bash
  docker logs server_gateway
  ```

- **Problemas con Grafana:**
  Asegúrate de que Grafana puede acceder a la base de datos MySQL mediante las credenciales configuradas.

---

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un *issue* o envía un *pull request* para discutir cambios importantes.

---

## Licencia

Este proyecto está bajo la Licencia MIT.

