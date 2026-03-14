# Story 4: Checkout & Payments

## Description
As a customer, I want to check out using Stripe so I can purchase educational materials securely.

## Acceptance Criteria
- Enter shipping address
- Guest checkout with email (no account required)
- Registered user checkout with saved info
- Stripe Elements for card input
- PaymentIntent created on backend
- Payment confirmation creates order
- Stripe webhook handles async payment events
- Idempotent order creation
- Inventory decremented on successful payment

## API Endpoints
- POST /api/checkout/
- POST /api/checkout/confirm/
- POST /api/webhook/stripe/

## Technical Notes
- Stripe PaymentIntent API
- Webhook signature verification
- Transaction atomicity for order creation + inventory update
