# Smart E-Commerce Platform

A backend-focused Smart E-Commerce Platform built using **FastAPI, Django, MySQL, JWT Authentication, Auth0, Stripe, WebSockets, and Email Notifications**.

## Project Overview

The platform provides APIs for customers to register and authenticate, browse products, manage their shopping cart, place orders, make payments, and receive notifications.

The Django backend provides administrative functionality for managing users, products, orders, analytics, and reports.

## Technology Stack

- **Backend:** FastAPI, Django
- **Database:** MySQL
- **ORM:** SQLAlchemy, Django ORM
- **Authentication:** JWT, Auth0
- **Payment:** Stripe
- **Notifications:** Email, WebSockets
- **API Testing:** Postman
- **Database Migration:** Alembic, Django Migrations
- **API Documentation:** FastAPI Swagger / OpenAPI

## User Panel – FastAPI

- User registration and login
- JWT authentication
- Role-based access control
- Google authentication using Auth0
- Product browsing
- Category-based product browsing
- Shopping cart management
- Order creation and order history
- Stripe Checkout payment integration
- Payment status handling
- In-app notifications
- Email notifications
- Real-time WebSocket notifications

## Admin Panel – Django

- Django Admin panel
- User management
- Product management
- Order management
- Order status management
- Sales analytics
- Revenue trends
- Top-selling products
- Low-stock product tracking
- CSV order reports
- PDF order reports

## Main Entities

- User
- Category
- Product
- Cart
- Order
- Order Item
- Payment
- Notification

## Database

The application uses **MySQL** as the primary database.

Database configuration is stored using environment variables in the `.env` file.

Sensitive configuration such as:

- Database password
- JWT secret
- Stripe keys
- Email credentials
- Auth0 credentials

is not committed to GitHub.

## Authentication & Security

- JWT authentication for protected FastAPI APIs
- Role-based access control for customer, staff, and admin users
- Auth0 integration for Google authentication
- Password hashing
- User ownership validation
- Environment variables for sensitive credentials
- Stripe payment processing without storing CVV information
- Protected administrative functionality

## Payment Integration

Stripe Checkout is integrated for payment processing.

The payment flow includes:

1. Create an order
2. Create Stripe Checkout Session
3. Complete payment through Stripe
4. Receive Stripe webhook
5. Update payment status
6. Send payment/order notifications

## Notifications

The platform supports:

- In-app notifications
- Email notifications
- Real-time WebSocket notifications
- Order confirmation notifications
- Shipping update notifications
- Payment failure notifications

## Analytics

The Django admin backend provides analytics APIs for:

- Total sales
- Total orders
- Top-selling products
- Revenue trends
- Low-stock products

## Reports

The platform supports exporting order information as:

- CSV
- PDF

## API Testing

A Postman collection is included in the `postman` folder.

The collection contains requests for:

- Authentication
- Auth0
- Categories
- Products
- Cart
- Orders
- Payments
- Notifications
- Analytics
- Reports

## Project Status

**Backend development completed with major e-commerce features implemented and API integrations tested.**

## Deliverables

- Django source code
- FastAPI source code
- Database migration files
- API implementation
- Stripe integration
- Auth0 integration
- WebSocket notifications
- Email notifications
- Postman API collection
- Analytics APIs
- CSV/PDF reporting
- Project documentation

## Project Structure

```text
smart_ecommerce/
│
├── django_backend/
│   ├── config/
│   ├── users/
│   └── orders/
│
├── fastapi_backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/
│   │   └── services/
│   │
│   └── alembic/
│
├── postman/
│   └── Smart E-Commerce API.postman_collection
│
└── .gitignore
