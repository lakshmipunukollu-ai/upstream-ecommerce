# Story 1: User Authentication

## Description
As a school administrator, I want to register and log in so I can manage my orders and get personalized recommendations.

## Acceptance Criteria
- User can register with email, password, first_name, last_name
- User can log in and receive JWT access + refresh tokens
- User can refresh expired access tokens
- User can view and update their profile
- User can create/update their district profile
- Passwords are hashed with Django's built-in hasher

## API Endpoints
- POST /api/accounts/register/
- POST /api/accounts/login/
- POST /api/accounts/token/refresh/
- GET /api/accounts/profile/
- PUT /api/accounts/profile/
- PUT /api/accounts/district-profile/

## Technical Notes
- Use djangorestframework-simplejwt for JWT handling
- Custom User model with email as username
- DistrictProfile model linked via OneToOne
