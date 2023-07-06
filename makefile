SHELL := /bin/bash

appsetup: dockerbuild setupdb

dockerbuild:
	docker system prune -f
	docker-compose build --no-cache

setupdb:
	docker-compose down -v
	docker-compose up -d postgres-db