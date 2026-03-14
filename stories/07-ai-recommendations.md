# Story 7: AI Curriculum Recommendations

## Description
As a registered user with a district profile, I want personalized curriculum recommendations based on my district's demographics and purchase history.

## Acceptance Criteria
- Recommendations based on district profile (ELL %, FRL %, grade levels)
- Considers purchase history to avoid duplicates
- Considers current cart contents
- Returns 3-5 product recommendations with reasons
- Each recommendation includes confidence score and grade levels served
- Graceful fallback if AI service unavailable

## API Endpoints
- GET /api/recommendations/

## Technical Notes
- Uses Anthropic Claude API
- Structured JSON output parsing
- Retry with exponential backoff
- Validates recommended product IDs exist in database
