# README

## to test the /items endpoint with args

curl "http://127.0.0.1:5000/items?start_date=2022-01-01T10:00:00&end_date=2025-01-25T10:00:00&category=Stationary"

## to test the /items-filter-page-sort endpoint

curl -X POST http://127.0.0.1:5000/items-filter-page-sort \
-H "Content-Type: application/json" \
-d '{
"filters": {"category": "Clothing"},
"pagination": {"page": 1, "limit": 5},
"sort": {"field": "last_updated_dt", "order": "desc"}
}'
