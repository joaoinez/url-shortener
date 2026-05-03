.PHONY: database-up
database-up:
	uv run alembic upgrade head

.PHONY: dev-docker
dev-docker:
	docker compose -f compose.dev.yml up --build

.PHONY: dev
dev:
	APP_ENV=development uv run fastapi dev
