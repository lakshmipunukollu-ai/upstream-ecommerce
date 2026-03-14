# Story 2: Product Catalog

## Description
As a visitor, I want to browse educational products with filtering and search so I can find the right materials for my district.

## Acceptance Criteria
- Products displayed in a grid/list view with images, title, price
- Filter by category and grade level
- Search by title/description
- Paginated results
- Product detail page with full description and availability
- Categories listed for navigation
- Admin can create/update/deactivate products

## API Endpoints
- GET /api/products/
- GET /api/products/{slug}/
- GET /api/products/categories/
- POST /api/products/ (admin)
- PUT /api/products/{slug}/ (admin)

## Technical Notes
- SlugField for SEO-friendly URLs
- JSONField for grade_levels and images
- Index on (category, is_active) for query performance
