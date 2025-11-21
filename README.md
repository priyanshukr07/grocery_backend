👥 Authentication & User Roles

JWT-based authentication (access + refresh tokens).

Two roles:

Customer – browse, cart, checkout, wishlist.

Manager – add/edit/delete products, categories, promo codes, sales reports.

Admin can promote a user to manager.

🛒 Customer Features

Browse products with:

Category filters

Search

Popularity sorting (most sold)

Manage cart (add, update, delete)

Checkout with auto stock reduction

Apply promo codes

Maintain wishlist

View orders

🏪 Manager Features

CRUD for:

Categories

Products

Product images (S3-compatible)

Promo codes

Low-stock alerts via Django signals

Sales report (most/least sold, filtered by category)

📦 Tech Stack

Django 5 + Django Rest Framework

PostgreSQL

JWT Authentication

AWS S3 Storage via django-storages

Docker/AWS EC2 compatible

Includes a complete Postman Collection & Environment files

Collection 

Env 

## 🗂️ Project Structure
```
grocery_backend/
│── manage.py
│── grocery_backend/
│ ├── settings.py
│ ├── urls.py
│ ├── asgi.py
│ └── wsgi.py
│
└── store/
├── models.py ← Complete DB schema
├── serializers.py ← Validation & API formatting
├── views.py ← Full business logic
├── permissions.py ← Role-based access
├── urls.py
├── signals.py ← Low-stock alerts
└── admin.py
```
# 🏗️ Database Design (UML Diagram)

```
+-----------------------+
|         User          |
+-----------------------+
| id (PK)               |
| username              |
| email                 |
| password              |
| role [customer/manager] 
+-----------------------+
          1
          |
          N
+-----------------------+
|        Order          |
+-----------------------+
| id (PK)               |
| customer_id (FK→User) |
| created_at            |
| total_amount          |
+-----------------------+
          1
          |
          N
+-----------------------------+
|         OrderItem           |
+-----------------------------+
| id (PK)                     |
| order_id (FK→Order)         |
| product_id (FK→Product)     |
| quantity                    |
| price_at_purchase           |
+-----------------------------+

+-----------------------+
|       Category        |
+-----------------------+
| id (PK)               |
| name                  |
| slug                  |
+-----------------------+
          1
          |
          N
+-----------------------+
|        Product        |
+-----------------------+
| id (PK)               |
| name                  |
| slug                  |
| category_id (FK)      |
| price                 |
| stock                 |
| created_at            |
+-----------------------+
          1
          |
          N
+-----------------------+
|     ProductImage      |
+-----------------------+
| id (PK)               |
| product_id (FK)       |
| image (S3 URL)        |
| created_at            |
+-----------------------+

+------------------------+
|       CartItem         |
+------------------------+
| id (PK)                |
| user_id (FK→User)      |
| product_id (FK→Product)|
| quantity               |
| added_at               |
+------------------------+

+------------------------+
|     WishlistItem       |
+------------------------+
| id (PK)                |
| user_id (FK→User)      |
| product_id (FK→Product)|
| added_at               |
+------------------------+

+------------------------+
|       PromoCode        |
+------------------------+
| id (PK)                |
| code (unique)          |
| discount_type          |
| value                  |
| is_active              |
| expires_at             |
+------------------------+

```

🔌 API Documentation
✔ Postman Collection

A complete Postman Collection with AUTH, Products, Categories, Cart, Wishlist, Promo Codes, Reports is included here:
Postman Collection →
Environment File →

⚙️ Setup & Installation
1️⃣ Clone the repository
git clone https://github.com/your-username/grocery-backend.git
cd grocery-backend

2️⃣ Install dependencies

(Dependencies based on requirements.txt )

pip install -r requirements.txt

3️⃣ Configure environment variables

Create a .env file:

# DJANGO SETTINGS

ALLOWED_HOSTS=<your_server_ip>,localhost,127.0.0.1
SECRET_KEY=<your_secret_key>

DEBUG=False


# DATABASE (PostgreSQL)

DB_NAME=<your_db_name>
DB_USER=<your_db_user>
DB_PASSWORD=<your_db_password>
DB_HOST=<your_db_host>
DB_PORT=5432


# AWS S3 CREDENTIALS

AWS_ACCESS_KEY_ID=<your_access_key>
AWS_SECRET_ACCESS_KEY=<your_secret_key>
AWS_STORAGE_BUCKET_NAME=<your_bucket_name>
AWS_REGION=ap-south-1

4️⃣ Run migrations
python manage.py migrate

5️⃣ Start server
python manage.py runserver

🧪 Tests

Unit/integration tests exist under store/tests.py and cover auth, product CRUD, cart, wishlist & checkout logic.
Tests file reference → .

Run tests:

python manage.py test

📊 Sales Reports

Managers can fetch sales analytics:

GET /api/reports/sales-by-product/


Supports:

?sort=most

?sort=least

?category=Fruits

☁ Deployment Notes

Fully compatible with:

AWS EC2 + Nginx + Gunicorn (WSGI)

AWS RDS for PostgreSQL

AWS S3 for media storage

Uses Django's production-ready settings from:
grocery_backend/settings.py
