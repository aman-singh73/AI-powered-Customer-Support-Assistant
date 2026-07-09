.PHONY: setup run test lint build docker-up docker-down clean

setup:
	pip install -r requirements.txt

run:
	uvicorn main:app --reload

test:
	pytest

lint:
	flake8 . && black --check .

build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

clean:
	docker-compose down
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
