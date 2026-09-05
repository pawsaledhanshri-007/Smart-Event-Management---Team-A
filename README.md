# Agentic AI Smart Event Management System - Backend

This is the production-ready REST API backend for the Agentic AI Smart Event Management System, built with Python, FastAPI, and PostgreSQL.

## Architecture & Technology Stack
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Authentication**: JWT & Passlib (bcrypt)
- **Validation**: Pydantic
- **Testing**: Pytest (SQLite in-memory)
- **Containerization**: Docker & Docker Compose

## Folder Structure
```
backend/
├── app/
│   ├── api/          # API Routers (auth, venues, events, registrations)
│   ├── core/         # Configuration, Security, JWT
│   ├── db/           # Database setup and base models
│   ├── models/       # SQLAlchemy ORM Models
│   ├── schemas/      # Pydantic validation schemas
│   └── main.py       # FastAPI application entry point
├── tests/            # Pytest test suites
├── alembic/          # Alembic database migrations
├── Dockerfile        # Docker image definition
├── docker-compose.yml# Docker compose for App & DB
├── requirements.txt  # Python dependencies
└── .env.example      # Example environment variables
```

## Setup Instructions

### 1. Environment Variables
Create a `.env` file from the example:
```bash
cp .env.example .env
```
Ensure `DATABASE_URL` matches your local PostgreSQL setup or use the default provided in `.env.example` if using Docker.

### 2. Run with Docker (Recommended)
This will spin up both the FastAPI backend and a PostgreSQL database.
```bash
docker-compose up --build
```
The API will be available at `http://localhost:8000`.

### 3. Local Installation (Without Docker)
1. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Setup Database Migrations:
   Make sure you have a running PostgreSQL database configured in your `.env` file. Then run:
   ```bash
   alembic upgrade head
   ```
4. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

### 4. Running Tests
Tests run using an in-memory SQLite database, so no external DB is needed.
```bash
pytest
```

## Database Migrations
To auto-generate a new migration after modifying `app/models/`:
```bash
alembic revision --autogenerate -m "Description"
```
To apply migrations:
```bash
alembic upgrade head
```

## API Documentation & Endpoints
Once the application is running, the interactive Swagger UI documentation is available at:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Key Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - Login to get JWT access token
- `GET /api/auth/me` - Get current user profile
- `GET, POST, PUT /api/venues` - Venue CRUD (Admin only for POST/PUT)
- `GET, POST, PUT, DELETE /api/events` - Event CRUD (Admin only for mutations)
- `POST /api/events/{id}/register` - Register for an event
- `GET /api/registrations/me` - View your registrations

## GitHub Setup Instructions
To push this project to GitHub:
```bash
git init
git add .
git commit -m "Initial commit of Event Management Backend"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```
