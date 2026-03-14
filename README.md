# Upstream Literacy E-Commerce

An e-commerce platform for educational literacy materials, serving K-8 school districts and administrators. Built with Django REST Framework (backend) and React + TypeScript (frontend).

## Features

- **Product Catalog**: Browse, search, and filter literacy curriculum materials by category and grade level
- **Shopping Cart**: Persistent cart for both authenticated users and guest sessions
- **Checkout**: Stripe-powered payment flow with guest checkout support
- **Order Management**: Order history and status tracking
- **User Accounts**: JWT authentication with district profile management
- **Inventory Management**: Admin dashboard for stock tracking and low-stock alerts
- **AI Recommendations**: Claude-powered curriculum recommendations based on district demographics and purchase history
- **Health Check**: GET /health endpoint for monitoring

## Tech Stack

- **Backend**: Django 5 + Django REST Framework
- **Frontend**: React 18 + TypeScript + Vite
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Auth**: JWT via djangorestframework-simplejwt
- **Payments**: Stripe (Payment Intents)
- **AI**: Anthropic Claude API

## Quick Start

```bash
# Setup Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

# Setup database
make migrate
make seed

# Install frontend dependencies
make frontend-install

# Run backend (port 3009)
make dev

# Run frontend (port 5009, in another terminal)
make frontend-dev
```

## Available Commands

| Command | Description |
|---------|-------------|
| `make dev` | Run Django backend on port 3009 |
| `make frontend-dev` | Run Vite frontend on port 5009 |
| `make test` | Run all backend tests |
| `make seed` | Seed database with sample data |
| `make migrate` | Run database migrations |
| `make build` | Production build (static files + frontend) |
| `make setup` | Full setup (migrate + seed + frontend install) |

## Test Users

| Email | Password | Role |
|-------|----------|------|
| admin@upstream.edu | admin123 | Admin |
| teacher@school.edu | teacher123 | Teacher |

## API Endpoints

- `GET /health` - Health check
- `POST /api/accounts/register/` - Register
- `POST /api/accounts/login/` - Login (returns JWT)
- `GET /api/products/` - List products
- `GET /api/products/{slug}/` - Product detail
- `GET /api/cart/` - Get cart
- `POST /api/cart/items/` - Add to cart
- `POST /api/checkout/` - Create payment intent
- `GET /api/orders/` - Order history
- `GET /api/inventory/` - Inventory (admin)
- `GET /api/recommendations/` - AI recommendations

## Environment Variables

Copy `.env.example` to `.env` and configure:
- `SECRET_KEY` - Django secret key
- `DATABASE_URL` - Database connection string
- `STRIPE_SECRET_KEY` - Stripe API key
- `ANTHROPIC_API_KEY` - Anthropic API key for AI recommendations
