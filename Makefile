VENV = .venv/bin

.PHONY: dev test seed build migrate frontend-install frontend-dev frontend-build setup

# Backend
dev:
	cd backend && ../$(VENV)/python manage.py runserver 3009

migrate:
	cd backend && ../$(VENV)/python manage.py makemigrations && ../$(VENV)/python manage.py migrate

seed:
	cd backend && ../$(VENV)/python manage.py seed

test:
	cd backend && ../$(VENV)/python manage.py test --verbosity=2

build:
	cd backend && ../$(VENV)/python manage.py collectstatic --noinput
	cd frontend && npm run build

# Frontend
frontend-install:
	cd frontend && npm install

frontend-dev:
	cd frontend && npm run dev

frontend-build:
	cd frontend && npm run build

# Setup
setup: migrate seed frontend-install
