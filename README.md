# Grocery Store Backend — Django REST API

A production-ready backend for an online grocery store built with Django, Django REST Framework, JWT authentication and AWS services (EC2, S3, RDS). Supports role-based access for Customers, Managers and Admins.

## Live Deployment
Base API URL:
```
http://65.0.92.157/api/
```
All endpoints (auth, products, cart, wishlist, checkout, reports) are available on the live server.

## Features

### Authentication & Roles
- JWT authentication (access + refresh tokens)
- Roles: Customer, Manager, Admin

### Customer
- Browse, search, filter and sort products
- Manage cart and wishlist
- Apply promo codes at checkout
- Checkout with stock validation and stock reduction
- View order history

### Manager
- CRUD for categories and products
- Manage product images (S3)
- Create promo codes
- Sales reports (most/least sold, filter by category)
- Low-stock alerts (Django signals)

### Admin
- Promote users to manager

## Tech Stack
- Django 5
- Django REST Framework
- SimpleJWT
- PostgreSQL
- AWS S3 (media)
- AWS EC2 (deployment)
- Nginx + Gunicorn

## Project Structure
```
grocery_backend/
├── manage.py
├── grocery_backend/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── store/
    ├── models.py        ← DB schema
    ├── serializers.py   ← API validation
    ├── views.py         ← Business logic
    ├── permissions.py   ← Role-based access
    ├── urls.py
    ├── signals.py       ← Low-stock alerts
    └── admin.py
```

## Database UML Diagram
Files:
- `/docs/grocery_backend_uml.drawio`
- `/docs/grocery_backend_uml.png`

Entities include User, Category, Product, ProductImage, CartItem, WishlistItem, Order & OrderItem, PromoCode.

## API Documentation & Postman
Postman collection and environment:
- `/docs/grocery_backend.postman_collection.json`
- `/docs/grocery_backend_environment.postman_environment.json`

Import the collection and environment, add JWT tokens to the environment variables, then test endpoints.

## Setup & Installation

1. Clone
```
git clone https://github.com/your-username/grocery-backend.git
cd grocery-backend
```

2. Install dependencies
```
pip install -r requirements.txt
```

3. Create `.env` and add environment variables

Django
```
ALLOWED_HOSTS=<your_server_ip>,localhost,127.0.0.1
SECRET_KEY=<your_secret_key>
```

PostgreSQL
```
DB_NAME=<your_db_name>
DB_USER=<your_db_user>
DB_PASSWORD=<your_db_password>
DB_HOST=<your_db_host>
DB_PORT=5432
```

AWS S3
```
AWS_ACCESS_KEY_ID=<your_access_key>
AWS_SECRET_ACCESS_KEY=<your_secret_key>
AWS_STORAGE_BUCKET_NAME=<your_bucket_name>
AWS_REGION=ap-south-1
```

4. Apply migrations
```
python manage.py migrate
```

5. Run development server
```
python manage.py runserver
```

## Tests
Unit & integration tests in:
```
store/tests.py
```
Run:
```
python manage.py test
```

## Sales Reports (Manager)
Endpoint:
```
GET /api/reports/sales-by-product/
```
Query params:
- `?sort=most`
- `?sort=least`
- `?category=Fruits`

## Deployment Notes
Production-ready configuration for:
- AWS EC2 + Nginx + Gunicorn
- AWS S3 (media)
- AWS RDS (PostgreSQL)
Environment-based settings in `grocery_backend/settings.py`.

## Additional
- Postman collection included for quick testing
- UML diagram included in `/docs`

