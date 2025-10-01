.PHONY: build run stop test clean logs shell

build:
	docker-compose build

run:
	docker-compose up -d

dev:
	docker-compose up

stop:
	docker-compose down

test:
	docker-compose exec app pytest src/tests/ -v

logs:
	docker-compose logs -f app

shell:
	docker-compose exec app /bin/bash

clean:
	docker-compose down --rmi all --volumes --remove-orphans

rebuild: clean build