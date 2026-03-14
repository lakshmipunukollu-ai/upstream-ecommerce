.PHONY: dev test seed build migrate frontend-install frontend-dev

# Backend
dev:
	cd backend && ../$(VENV)/python manage.py runserver

migrate:
	cd backend && ../$(VENV)/python manage.py makemigrations && ../$(VENV)/python manage.py migrate

seed:
	cd backend && ../$(VENV)/python manage.py seed

test:
	cd backend && ../$(VENV)/python manage.py test --verbosity=2

build:
	cd backend && ../$(VENV)/python manage.py collectstatic --noinput

# Frontend
frontend-install:
	cd frontend && npm install

frontend-dev:
	cd frontend && npm run dev

# Setup
setup: migrate seed

VENV = .venv/bin
