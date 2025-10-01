.PHONY: build run stop test clean logs shell

build:
	docker build -t app .

run:
	docker run -d --name app -p 8000:8000 --env-file .env app

dev:
	docker run --name app -p 8000:8000 --env-file .env app

stop:
	docker stop app && docker rm app

test:
	docker run --rm --env-file .env app pytest src/tests/ -v

logs:
	docker logs -f app

shell:
	docker exec -it app /bin/bash

clean:
	docker stop app 2>/dev/null || true
	docker rm app 2>/dev/null || true
	docker rmi app 2>/dev/null || true

rebuild: clean build