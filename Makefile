.PHONY: docker-up
docker-up:
	docker compose --env-file backend/.env up --build --wait

.PHONY: docker-down
docker-down:
	docker compose --env-file backend/.env down

.PHONY: run-back
run-back:
	uv run --directory backend uvicorn app.main:app --reload

.PHONY: test-back
test-back:
	uv run --directory backend python -m pytest -v

.PHONY: format-back
format-back:
	uv run --directory backend ruff format .

.PHONY: format-back-check
format-back-check:
	uv run --directory backend ruff format --check .

.PHONY: lint-back
lint-back:
	uv run --directory backend ruff check .

.PHONY: fix-back
fix-back:
	uv run --directory backend ruff check --fix .
	uv run --directory backend ruff format .


.PHONY: format-front
format-front:
	npm --prefix frontend run format

.PHONY: format-front-check
format-front-check:
	npm --prefix frontend run format:check

.PHONY: lint-front
lint-front:
	npm --prefix frontend run lint

.PHONY: fix-front
fix-front:
	npm --prefix frontend run lint:fix
	npm --prefix frontend run format

.PHONY: build-front
build-front:
	npm --prefix frontend run build


.PHONY: lint
lint: lint-back lint-front

.PHONY: check
check: format-back-check lint-back format-front-check lint-front build-front

.PHONY: fix
fix: fix-back fix-front