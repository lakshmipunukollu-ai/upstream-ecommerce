# Story 6: Inventory Management

## Description
As an admin, I want to track stock levels and get alerts for low-stock items.

## Acceptance Criteria
- View all product stock levels
- Low-stock alerts (threshold: 10 units)
- Update stock levels manually
- Stock decremented on order placement
- Prevent overselling (stock validation)

## API Endpoints
- GET /api/inventory/
- GET /api/inventory/low-stock/
- PUT /api/inventory/{product_id}/

## Technical Notes
- Admin-only endpoints
- Atomic stock decrement with F() expressions
- Low stock threshold configurable
