# Coderr Backend

Coderr is a Django REST Framework backend for a freelance marketplace platform. It provides token-based authentication, user profiles, service offers, offer packages, orders, reviews, and basic platform statistics.

## Features

- User registration and login with DRF token authentication
- Customer and business user profiles
- Offer management with package tiers: basic, standard, and premium
- Order creation and order status tracking
- Review system for business users
- Basic platform statistics endpoint
- Filtering support through `django-filter`
- CORS configuration for local frontend development

## Tech Stack

- Python
- Django 6
- Django REST Framework
- SQLite for local development
- django-filter
- django-cors-headers

## Project Structure

```text
coderr/
+-- auth_app/          # Registration and login API
+-- core/              # Django project settings and root URLs
+-- offers_app/        # Offers and offer package details
+-- orders_app/        # Orders and order statistics
+-- page_info_app/     # Basic platform information
+-- profile_app/       # User profile management
+-- reviews_app/       # Business user reviews
+-- manage.py
+-- requirements.txt
```

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd coderr
```

### 2. Create and activate a virtual environment

On Windows:

```bash
python -m venv env
env\Scripts\activate
```

On macOS/Linux:

```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create an admin user

```bash
python manage.py createsuperuser
```

### 6. Start the development server

```bash
python manage.py runserver
```

The API will be available at:

```text
http://127.0.0.1:8000/api/
```

The Django admin is available at:

```text
http://127.0.0.1:8000/admin/
```

## Local Development Settings

The project currently allows local backend hosts:

```python
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
```

For local frontend development, CORS is configured for:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]
```

If your frontend runs on another port, add that origin to `CORS_ALLOWED_ORIGINS`.

## Authentication

The API uses token authentication.

After registration or login, the response contains a token. Send this token with protected requests:

```http
Authorization: Token <your-token>
```

Most endpoints require authentication by default.

## API Endpoints

### Authentication

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/api/registration/` | Register a new user |
| POST | `/api/login/` | Log in and receive an auth token |

### Profiles

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/profile/` | List user profiles |
| GET | `/api/profile/<id>/` | Retrieve a user profile |
| PATCH/PUT | `/api/profile/<id>/` | Update a user profile |

### Offers

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/offers/` | List offers |
| POST | `/api/offers/` | Create an offer |
| GET | `/api/offers/<id>/` | Retrieve an offer |
| PATCH/PUT | `/api/offers/<id>/` | Update an offer |
| DELETE | `/api/offers/<id>/` | Delete an offer |
| GET | `/api/offerdetails/` | List offer package details |
| GET | `/api/offerdetails/<id>/` | Retrieve an offer package detail |

### Orders

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/orders/` | List orders |
| POST | `/api/orders/` | Create an order |
| GET | `/api/orders/<id>/` | Retrieve an order |
| PATCH/PUT | `/api/orders/<id>/` | Update an order |
| DELETE | `/api/orders/<id>/` | Delete an order |
| GET | `/api/order-count/<business_user_id>/` | Count active orders for a business user |
| GET | `/api/completed-order-count/<business_user_id>/` | Count completed orders for a business user |

### Reviews

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/reviews/` | List reviews |
| POST | `/api/reviews/` | Create a review |
| GET | `/api/reviews/<id>/` | Retrieve a review |
| PATCH/PUT | `/api/reviews/<id>/` | Update a review |
| DELETE | `/api/reviews/<id>/` | Delete a review |

### Page Info

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/api/base-info/` | Retrieve basic platform statistics |