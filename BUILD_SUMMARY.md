# Build Summary - Upstream Literacy E-Commerce

## Project Overview
Full-stack e-commerce platform for educational literacy materials targeting K-8 school districts.

## Architecture
- **Backend**: Django 5 + Django REST Framework on port 3009
- **Frontend**: React 18 + TypeScript + Vite on port 5009
- **Database**: SQLite (dev), PostgreSQL-ready (production)
- **Auth**: JWT via djangorestframework-simplejwt
- **Payments**: Stripe integration (Payment Intents)
- **AI**: Anthropic Claude API for curriculum recommendations

## Backend Apps
| App | Models | Endpoints | Description |
|-----|--------|-----------|-------------|
| accounts | User, DistrictProfile | 5 | JWT auth, user profiles, district demographics |
| products | Category, Product | 6 | CRUD catalog with search, filtering by category/grade |
| cart | Cart, CartItem | 5 | Session-based guest + authenticated user carts |
| orders | Order, OrderItem | 5 | Checkout flow, Stripe webhooks, order history |
| inventory | (uses Product) | 3 | Stock levels, low-stock alerts, admin stock updates |
| recommendations | (uses multiple) | 1 | AI-powered curriculum suggestions with fallback |

## Frontend Pages
- Home (featured products)
- Product List (with search/filter)
- Product Detail (with add-to-cart)
- Shopping Cart (quantity management)
- Checkout (shipping address form)
- Order Confirmation
- Order History
- Login / Register
- Profile (personal + district info)
- Inventory Management (admin)
- AI Recommendations

## Test Coverage
- **56 total tests** across all backend apps
- All tests pass (`make test` exits 0)
- 1 test skipped (SQLite JSON contains limitation)
- Coverage: models, views, serializers, permissions, seed command, health check

## Seed Data
- 6 categories (Phonics, Reading Comprehension, Writing, Vocabulary, ELL/Bilingual, Intervention)
- 10 products with realistic literacy curriculum descriptions
- 2 users (admin + teacher with district profile)

## Key Decisions
1. SQLite for development, PostgreSQL-ready via dj-database-url
2. UUID primary keys on all models for security
3. Session-based guest carts for unauthenticated users
4. Soft-delete for products (is_active flag)
5. Fallback recommendations when AI API unavailable
6. Inline styles for frontend (no external CSS framework dependency)
