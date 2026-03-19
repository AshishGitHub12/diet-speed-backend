# Diet Speed Backend

A Django REST API for a fitness tracking application that includes:

- User authentication (JWT)
- Profile & onboarding system
- Weight tracking with graph-ready APIs
- Home dashboard API

## Tech Stack

- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication

## Setup Instructions

### 1. Clone repo

git clone <repo-url>

cd diet-speed-backend

### 2. Create virtual environment

python3 -m venv venv

source venv/bin/activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Setup environment variables

Create a `.env` file:

SECRET_KEY=django-insecure-yjpvtsp-wk(+#b%9l@rlini_uae!75r)cgskgz@d-&zl6do7&e

DEBUG=True

ALLOWED_HOSTS=127.0.0.1,localhost

DB_NAME=diet_speed

DB_USER=postgres

DB_PASSWORD=331212

DB_HOST=localhost

DB_PORT=5432

### 5. Run migrations

python manage.py makemigrations

python manage.py migrate

### 6. Run server

python manage.py runserver
