# Upstream Literacy E-Commerce — Architecture Document

## Overview
Upstream Literacy is an e-commerce checkout system for educational materials serving school districts and administrators. The platform provides product catalog browsing, persistent shopping cart, Stripe-powered checkout (guest + registered), order management, inventory tracking, and AI-powered curriculum recommendations.

## Stack
| Layer | Technology |
|-------|-----------|
| Backend | Django 5 + Django REST Framework |
| Frontend | React 18 + TypeScript + Vite |
| Database | PostgreSQL 15 |
| Payments | Stripe (Payment Intents + Elements) |
| Auth | JWT (djangorestframework-simplejwt) |
| AI | Anthropic Claude API (curriculum recommendations) |
| Deploy Target | Render |

## System Architecture
```
┌─────────────────────────────────────────────────────┐
│                    Render                            │
│  ┌──────────────────┐    ┌───────────────────────┐  │
│  │  React Frontend   │───▶│  Django API Server    │  │
│  │  (Vite build)     │    │  (Gunicorn + DRF)     │  │
│  └──────────────────┘    └───────┬───────────────┘  │
│                                  │                   │
│                          ┌───────▼───────┐           │
│                          │  PostgreSQL   │           │
│                          └───────────────┘           │
│                                                      │
│  External:  Stripe API  |  Anthropic Claude API      │
└─────────────────────────────────────────────────────┘
```

## Project Structure
```
upstream-ecommerce/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── upstream/              # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── products/              # Product catalog app
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── cart/                  # Shopping cart app
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── orders/                # Orders & checkout app
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── accounts/              # User accounts app
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── inventory/             # Inventory management app
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── recommendations/       # AI recommendations app
│   │   ├── models.py
│   │   ├── views.py
│   │   └── urls.py
│   └── shared/                # Shared utilities
│       ├── llm_client.py
│       └── auth.py
├── frontend/
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── index.html
│   └── src/
│       ├── App.tsx
│       ├── main.tsx
│       ├── api/               # API client
│       ├── components/        # Reusable components
│       ├── pages/             # Page components
│       ├── hooks/             # Custom hooks
│       ├── types/             # TypeScript types
│       └── store/             # State management
├── Makefile
├── .env.example
└── docker-compose.yml
```

## Data Models

### Category
| Field | Type | Notes |
|-------|------|-------|
| id | UUID (PK) | Auto-generated |
| name | CharField(100) | Required |
| slug | SlugField | Unique |
| description | TextField | Optional |
| parent | ForeignKey(self) | Nullable, for subcategories |
| created_at | DateTimeField | Auto |

### Product
| Field | Type | Notes |
|-------|------|-------|
| id | UUID (PK) | Auto-generated |
| title | CharField(200) | Required |
| slug | SlugField | Unique |
| description | TextField | Rich description |
| price | DecimalField(10,2) | Required |
| stock | PositiveIntegerField | Default 0 |
| category | ForeignKey(Category) | PROTECT on delete |
| grade_levels | JSONField | e.g. ["K","1","2","3"] |
| images | JSONField | List of image URLs |
| is_active | BooleanField | Default True |
| created_at | DateTimeField | Auto |
| updated_at | DateTimeField | Auto |

### Cart / CartItem
| Field | Type | Notes |
|-------|------|-------|
| Cart.id | UUID (PK) | |
| Cart.user | ForeignKey(User) | Nullable (guest carts via session) |
| Cart.session_key | CharField | For guest carts |
| Cart.created_at | DateTimeField | Auto |
| CartItem.cart | ForeignKey(Cart) | CASCADE |
| CartItem.product | ForeignKey(Product) | CASCADE |
| CartItem.quantity | PositiveIntegerField | Min 1 |

### Order / OrderItem
| Field | Type | Notes |
|-------|------|-------|
| Order.id | UUID (PK) | |
| Order.user | ForeignKey(User) | Nullable (guest checkout) |
| Order.guest_email | EmailField | Nullable |
| Order.status | CharField(20) | Choices: pending, paid, shipped, delivered, cancelled |
| Order.stripe_payment_intent | CharField(200) | Unique |
| Order.total | DecimalField(10,2) | |
| Order.shipping_address | JSONField | |
| Order.created_at | DateTimeField | Auto |
| OrderItem.order | ForeignKey(Order) | CASCADE |
| OrderItem.product | ForeignKey(Product) | PROTECT |
| OrderItem.quantity | PositiveIntegerField | |
| OrderItem.unit_price | DecimalField(10,2) | Snapshot at order time |

### DistrictProfile
| Field | Type | Notes |
|-------|------|-------|
| id | UUID (PK) | |
| user | OneToOneField(User) | |
| district_name | CharField(200) | |
| state | CharField(2) | US state code |
| student_count | IntegerField | |
| ell_percentage | DecimalField(5,2) | ELL student % |
| free_reduced_lunch_pct | DecimalField(5,2) | FRL % |
| grade_levels_served | JSONField | e.g. ["K","1","2"] |

## API Contracts

### Authentication — `/api/accounts/`
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /api/accounts/register/ | None | Register new user |
| POST | /api/accounts/login/ | None | Login, returns JWT pair |
| POST | /api/accounts/token/refresh/ | None | Refresh JWT |
| GET | /api/accounts/profile/ | JWT | Get user profile |
| PUT | /api/accounts/profile/ | JWT | Update profile |
| PUT | /api/accounts/district-profile/ | JWT | Update district profile |

#### POST /api/accounts/register/
```json
Request: { "email": "admin@school.edu", "password": "...", "first_name": "Jane", "last_name": "Doe" }
Response 201: { "id": "uuid", "email": "...", "tokens": { "access": "...", "refresh": "..." } }
```

#### POST /api/accounts/login/
```json
Request: { "email": "admin@school.edu", "password": "..." }
Response 200: { "access": "jwt...", "refresh": "jwt..." }
```

### Products — `/api/products/`
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /api/products/ | None | List products (paginated, filterable) |
| GET | /api/products/{slug}/ | None | Product detail |
| GET | /api/products/categories/ | None | List categories |
| POST | /api/products/ | Admin | Create product |
| PUT | /api/products/{slug}/ | Admin | Update product |
| DELETE | /api/products/{slug}/ | Admin | Deactivate product |

#### GET /api/products/?category=&grade_level=&search=&page=
```json
Response 200: {
  "count": 42,
  "next": "?page=2",
  "results": [
    {
      "id": "uuid", "title": "...", "slug": "...", "price": "29.99",
      "stock": 150, "category": { "id": "uuid", "name": "..." },
      "grade_levels": ["K","1"], "images": ["url1"], "is_active": true
    }
  ]
}
```

### Cart — `/api/cart/`
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /api/cart/ | Optional | Get current cart |
| POST | /api/cart/items/ | Optional | Add item to cart |
| PUT | /api/cart/items/{id}/ | Optional | Update item quantity |
| DELETE | /api/cart/items/{id}/ | Optional | Remove item |
| DELETE | /api/cart/ | Optional | Clear cart |

#### POST /api/cart/items/
```json
Request: { "product_id": "uuid", "quantity": 2 }
Response 201: { "id": "uuid", "product": {...}, "quantity": 2 }
```

### Checkout & Orders — `/api/orders/`
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /api/checkout/ | Optional | Create Stripe PaymentIntent |
| POST | /api/checkout/confirm/ | Optional | Confirm payment, create order |
| POST | /api/webhook/stripe/ | None (Stripe sig) | Stripe webhook handler |
| GET | /api/orders/ | JWT | List user's orders |
| GET | /api/orders/{id}/ | JWT | Order detail |

#### POST /api/checkout/
```json
Request: {
  "shipping_address": { "line1": "...", "city": "...", "state": "...", "zip": "..." },
  "guest_email": "optional@email.com"
}
Response 200: { "client_secret": "pi_xxx_secret_xxx", "order_id": "uuid" }
```

### Inventory — `/api/inventory/`
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /api/inventory/ | Admin | List all stock levels |
| GET | /api/inventory/low-stock/ | Admin | Products with low stock |
| PUT | /api/inventory/{product_id}/ | Admin | Update stock level |

### Recommendations — `/api/recommendations/`
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /api/recommendations/ | JWT | Get AI recommendations |

#### GET /api/recommendations/
```json
Response 200: {
  "recommendations": [
    {
      "product": { "id": "uuid", "title": "...", "price": "..." },
      "reason": "Complements your K-2 phonics materials with Grade 3 fluency practice",
      "confidence": 0.87,
      "grade_levels_served": ["3","4"]
    }
  ]
}
```

### Health — `/health`
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /health | None | Health check, returns 200 |

```json
Response 200: { "status": "healthy", "database": "connected" }
```

## Authentication Flow
1. User registers or logs in via `/api/accounts/`
2. Server returns JWT access + refresh tokens (via djangorestframework-simplejwt)
3. Frontend stores tokens in localStorage
4. All authenticated requests include `Authorization: Bearer <access_token>`
5. Token refresh via `/api/accounts/token/refresh/`
6. Guest checkout: no auth required for cart + checkout endpoints

## Payment Flow (Stripe)
1. User fills cart and proceeds to checkout
2. Frontend sends shipping address to `POST /api/checkout/`
3. Backend creates Stripe PaymentIntent, returns `client_secret`
4. Frontend uses Stripe Elements to collect card details
5. Frontend confirms payment with Stripe.js using `client_secret`
6. Stripe webhook fires `payment_intent.succeeded` to `/api/webhook/stripe/`
7. Backend webhook handler: creates Order, decrements inventory, clears cart

## AI Recommendations Flow
1. Authenticated user requests recommendations via `GET /api/recommendations/`
2. Backend loads user's DistrictProfile and purchase history
3. Backend constructs prompt with district demographics + purchase history + current cart
4. Claude API returns structured recommendations (product IDs, reasons, confidence)
5. Backend validates product IDs exist and are in stock
6. Returns formatted recommendations to frontend

## Environment Variables (.env)
```
SECRET_KEY=django-secret-key
DEBUG=True
DATABASE_URL=postgres://user:pass@localhost:5432/upstream
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
ANTHROPIC_API_KEY=sk-ant-...
JWT_SECRET=jwt-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

## Deviations from Brief
1. **Auth**: Using `djangorestframework-simplejwt` instead of `python-jose` + `passlib` from shared/auth.py — the shared auth module is FastAPI-specific. Django has its own auth system and simplejwt is the standard JWT solution for DRF.
2. **UUIDs as PKs**: Using UUIDs for all model primary keys for better security (no sequential ID enumeration).
3. **Session-based guest carts**: Using Django session keys for guest cart persistence rather than requiring authentication.
