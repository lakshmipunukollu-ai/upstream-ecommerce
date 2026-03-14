# Story 5: Order Management

## Description
As a registered user, I want to view my order history and track order status.

## Acceptance Criteria
- List all user orders with status
- View order detail with items
- Order status: pending, paid, shipped, delivered, cancelled
- Order contains shipping address, total, items with prices

## API Endpoints
- GET /api/orders/
- GET /api/orders/{id}/

## Technical Notes
- Orders linked to user or guest_email
- OrderItem stores unit_price snapshot
- State machine for status transitions
