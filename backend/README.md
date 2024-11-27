# Guide to testing endpoints directly with cURL

You are able to test a limited functionality end-to-end with the React frontend user interface. 
However, some backend functionality can only be tested via cURL commands at this point.

## to test the /items endpoint with args

Run `curl http://127.0.0.1:5000/items?start_date=2022-01-01T10:00:00&end_date=2025-01-25T10:00:00&category=Stationary`

Feel free to use different args for the `start_date`, `end_date` and `category` fields.


## to test the /items-filter-page-sort endpoint

Run 
```bash
curl -X POST http://127.0.0.1:5000/items-filter-page-sort \
-H 'Content-Type: application/json' \
-d '{"filters": {"category": "Clothing"}, "pagination": {"page": 1, "limit": 5}, "sort": {"field": "price", "order": "asc"}}'
```

Feel free to use different args for the `filters`, `pagination` and `sort` fields.


# Guide to running tests

## to run the pytests

Run `poetry run pytest`
