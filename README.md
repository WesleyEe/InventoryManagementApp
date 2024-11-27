# Guide to run application

## Prerequisites
1. Ensure Docker is installed
2. Ensure poetry is installed (for backend)
3. Ensure npm and node is installed (for frontend)

## DATABASE: Start up MySQL database
1. Enter database directory
- Run `cd database`

2. Start up database
- Run `docker-compose up`

## BACKEND: Start up Flask backend server
1. Enter backend directory
- Run `cd backend`

2. Install dependencies
- Run `poetry install`

3. Start up Flask server
- Run `poetry run python3 run.py`

> Refer to backend/README.md to find out how to query backend directly

## FRONTEND: Start up React frontend
1. Enter database directory
- Run `cd database`

2. Install dependencies
- Run `npm install`

3. Start up React frontend
- Run `npm start`

4. Go to http://localhost:5173/ on your Chrome browser (or any browser).