#!/bin/sh
echo "Init migrations"
until alembic upgrade head
do
  echo "Waiting for init migrations..."
  sleep 2
done
alembic check > /dev/null 2>&1
if ! [ $? -eq 0 ]; then
echo "Creating migrations"
until alembic revision --autogenerate
do
  echo "Waiting for create migrations..."
  sleep 2
done
fi
echo "Applying migrations"
until alembic upgrade head
do
  echo "Waiting for apply migrations..."
  sleep 2
done
exec "$@"