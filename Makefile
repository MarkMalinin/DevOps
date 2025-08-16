
.PHONY: up down logs ps bash test

up:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f

ps:
	docker compose ps

bash:
	docker compose exec backend bash

test:
	pytest -q
