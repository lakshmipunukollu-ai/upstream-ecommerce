# Story 8: Health Check

## Description
As a deployment system, I need a health endpoint to verify the service is running.

## Acceptance Criteria
- GET /health returns 200 with {"status": "healthy", "database": "connected"}
- Checks database connectivity
- No authentication required

## API Endpoints
- GET /health
