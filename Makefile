COMPOSE := docker compose -p teambus -f docker-compose.dev.yml

.PHONY: dev-db dev-db-down lint fmt test test-unit test-integration run migrate

dev-db:
	$(COMPOSE) up -d --wait db

dev-db-down:
	$(COMPOSE) down

lint:
	uv run ruff check .
	uv run ruff format --check .

fmt:
	uv run ruff check --fix .
	uv run ruff format .

test:
	uv run pytest

test-unit:
	uv run pytest -m "not integration"

test-integration:
	uv run pytest -m integration

run:
	uv run uvicorn teambus.api.app:create_app --factory --reload --port 8700

migrate:
	uv run teambus db migrate
