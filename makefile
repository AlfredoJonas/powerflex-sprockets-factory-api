SHELL := /bin/bash

appsetup: dockerbuild setupdb

makemigrations: python manage.py makemigrations

migrate:
	python manage.py migrate

loadfixtures:
	python manage.py build_factory_data

dockerbuild:
	docker system prune -f
	docker-compose build --no-cache

setupdb:
	docker-compose down -v
	docker volume rm -f powerflex-sprockets-factory-api_db_data || true
	docker-compose up -d postgres-db
	docker-compose run sprocket-api make migrate loadfixtures
