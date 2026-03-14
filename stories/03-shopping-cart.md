# Story 3: Shopping Cart

## Description
As a visitor or logged-in user, I want a persistent shopping cart so I can add products and review before checkout.

## Acceptance Criteria
- Add products to cart with quantity
- Update item quantities
- Remove items from cart
- Clear entire cart
- Cart persists across page refreshes
- Guest carts use session key
- Authenticated carts linked to user
- Cart shows subtotal

## API Endpoints
- GET /api/cart/
- POST /api/cart/items/
- PUT /api/cart/items/{id}/
- DELETE /api/cart/items/{id}/
- DELETE /api/cart/

## Technical Notes
- Optimistic UI updates on frontend
- Session key for guest identification
- Stock validation on add/update
