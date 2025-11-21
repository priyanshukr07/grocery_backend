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

AWS EC2 compatible

Includes a complete Postman Collection & Environment files

Inclueds a 

# 🗂️ Project Structure
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

🗂️ Database UML Diagram

A comprehensive UML class diagram has been created to showcase the full data model for the Grocery Store Backend.
It captures all core entities such as Users, Categories, Products, Orders, Cart Items, Wishlist Items, Promo Codes, and associated relationships.

🔗 UML Diagram File
```
/docs/grocery_backend_uml.drawio
Visual PNG version (optional): /docs/grocery_backend_uml.png
```
📌 What This Diagram Represents

Logical data model for the entire backend

Entity attributes & associations

One-to-many & many-to-one mappings

Catalog, Commerce, and User domains

Visual understanding of how the backend behaves end-to-end

This artifact ensures every contributor can quickly understand the structural blueprint and maintain consistency across development workflows.

🔌 API Documentation

🧪 Postman Collection

A full-featured Postman Collection is included to help developers test and validate all API endpoints with minimal setup.

🗂 Available Endpoints Include:

Auth: Register, Login, Refresh, Create Manager

Products: CRUD operations + image upload

Categories: CRUD (manager-only)

Cart: Add, Update, View, Checkout

Wishlist: Add, View, Remove

Promo Codes: CRUD

Reports: Sales by Product (manager-only)

🔗 Files Included
```
Postman Collection:
/docs/grocery_backend.postman_collection.json

Environment File:
/docs/grocery_backend_environment.postman_environment.json
```

💡 How to Use

Import the collection into Postman

Import the environment file

Add JWT tokens under environment variables

Start hitting endpoints instantly

This ensures smooth testing, faster debugging cycles, and predictable results across different developers and environments.

⚙️ Setup & Installation
1️⃣ Clone the repository
```
git clone https://github.com/your-username/grocery-backend.git
cd grocery-backend
```

2️⃣ Install dependencies

(Dependencies based on requirements.txt )
```
pip install -r requirements.txt
```

3️⃣ Configure environment variables

Create a .env file:

# DJANGO SETTINGS
```
ALLOWED_HOSTS=<your_server_ip>,localhost,127.0.0.1
SECRET_KEY=<your_secret_key>
```

# DATABASE (PostgreSQL)
```
DB_NAME=<your_db_name>
DB_USER=<your_db_user>
DB_PASSWORD=<your_db_password>
DB_HOST=<your_db_host>
DB_PORT=5432
```
# AWS S3 CREDENTIALS
```
AWS_ACCESS_KEY_ID=<your_access_key>
AWS_SECRET_ACCESS_KEY=<your_secret_key>
AWS_STORAGE_BUCKET_NAME=<your_bucket_name>
AWS_REGION=ap-south-1
```

4️⃣ Run migrations
```
python manage.py migrate
```

5️⃣ Start server
```
python manage.py runserver
```

🧪 Tests

Unit/integration tests exist under store/tests.py and cover auth, product CRUD, cart, wishlist & checkout logic.
Tests file reference → .

Run tests:
```
python manage.py test
```

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
```
grocery_backend/settings.py
```
