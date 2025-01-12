#!/bin/bash
# Espera hasta que el contenedor MySQL esté listo para aceptar conexiones

host="$1"
shift
cmd="$@"

until mysql -h"$host" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" -e 'select 1'; do
  >&2 echo "MySQL no está listo, esperando..."
  sleep 1
done

>&2 echo "MySQL está listo, ejecutando el comando..."
exec $cmd
