# Linear Algebra Interactive Book - Backend API

FastAPI-based backend for solution verification and grading.

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Run server
python run.py
```

Server will be available at `http://localhost:8000`
API docs at `http://localhost:8000/docs`

## API Endpoints

### Health
- `GET /api/v1/health` - Health check

### Problems
- `GET /api/v1/problems/{problem_id}` - Get problem details
- `GET /api/v1/problems/section/{section}` - Get all problems in a section
- `POST /api/v1/problems` - Create a new problem

### Submissions
- `POST /api/v1/submit/code` - Submit code solution
- `POST /api/v1/submit/math` - Submit mathematical answer
- `POST /api/v1/submit/multiple-choice` - Submit multiple choice answer

## Database

Uses SQLite by default (configured in `.env`). Can be changed to PostgreSQL.

## Project Structure

```
backend/
├── app/
│   ├── main.py          # FastAPI app entry point
│   ├── config.py        # Configuration
│   ├── db.py            # Database connection
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── routes/          # API route handlers
│   │   ├── health.py
│   │   ├── problems.py
│   │   └── submissions.py
│   └── services/        # Business logic
│       └── grader.py
├── tests/               # Unit tests
├── run.py              # Application entry point
├── requirements.txt    # Python dependencies
└── .env.example       # Environment variables template
```
