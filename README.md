# Vitalyx Supplement

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-000000?logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00?logo=sqlalchemy&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

A modular e-commerce web application built with **Python** and **Flask** for managing and selling health supplements. It supports user authentication, a database-backed shopping cart, checkout and order tracking, manual payment submission and verification, and a dedicated admin management panel.

---

## Features

- **Product Catalog:** Browse supplements by category and view detailed product pages.
- **User Authentication:** Account registration (`signup`) and login flows powered by `Flask-Login` and `Flask-WTF`.
- **Persistent Shopping Cart:** Add, update quantities, and remove items stored directly in the database.
- **Checkout & Order Management:** Complete checkout, place orders, and track order history and statuses (`my_orders`, `order_detail`).
- **Manual Payment Workflow:** Customers can submit payment details for their orders, followed by admin verification and status updates.
- **Admin Panel:** Administrative interface built with `Flask-Admin` for reviewing and managing orders, payments, products, and categories.
- **Rate Limiting & Form Protection:** Request throttling via `Flask-Limiter` and CSRF protection via `Flask-WTF`.
- **Custom Error Pages:** Styled error templates for HTTP `403`, `404`, and `502` responses.
- **Database Migrations:** Version-controlled schema evolution managed via Alembic (`Flask-Migrate`).

---

## Application Flow

1. **Customer Journey:** Browse catalog → View product details → Add to cart → Proceed to checkout → Submit payment proof → Track order status.
2. **Admin Journey:** Access admin panel → Review incoming orders & submitted payments → Approve/reject payments and update order statuses.

---

## Tech Stack

- **Backend:** Python, Flask, Flask-Login, Flask-Admin, Flask-Limiter
- **Database & ORM:** SQLAlchemy, Alembic (Flask-Migrate)
- **Forms & Validation:** Flask-WTF, WTForms
- **Frontend:** Jinja2 Templates, HTML5, CSS3, Vanilla JavaScript

---

## Project Structure

```text
vitalyx-supplement/
├── app/
│   ├── __init__.py          # Application factory and blueprint registration
│   ├── config.py            # Environment-based configuration
│   ├── extensions.py        # Flask extensions initialization
│   ├── admin_panel/         # Flask-Admin setup and custom views
│   ├── forms/               # Auth, checkout, and payment forms
│   ├── models/              # SQLAlchemy models (User, Product, Category, Cart, Order, Payment)
│   ├── routes/              # Blueprints (main, auth, cart, checkout, order, payments)
│   ├── static/              # CSS, JS, and static images
│   └── templates/           # Jinja2 HTML templates (storefront, admin, errors)
├── migrations/              # Alembic database migration scripts
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
└── .gitignore
```

---

## Getting Started

### Prerequisites

- Python 3.10+ (recommended)
- `pip` and `venv`

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/alireza-oman/vitalyx-supplement.git
   cd vitalyx-supplement
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate

   # Windows
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///db.sqlite3
   APP_ENV=development
   ```
   > **Security Note:** Never commit your `.env` file or real credentials to Git.

5. **Run database migrations:**
   ```bash
   # Linux / macOS
   export FLASK_APP=run.py
   flask db upgrade

   # Windows (Command Prompt)
   set FLASK_APP=run.py
   flask db upgrade

   # Windows (PowerShell)
   $env:FLASK_APP="run.py"
   flask db upgrade
   ```

6. **Start the application:**
   ```bash
   python run.py
   ```
   The application will be available at `http://127.0.0.1:5000`.

---

## Database Models Overview

| Model | Description |
| :--- | :--- |
| `User` | Registered customer and admin accounts |
| `Category` | Supplement categories |
| `Product` | Store items with pricing, details, and image paths |
| `Cart` & `CartItem` | Persistent user shopping carts and line items |
| `Order` & `OrderItem` | Customer orders, line items, and review/payment statuses |
| `Payment` | Submitted payment records linked to orders |

---

## Roadmap / Future Improvements

- [ ] Add automated unit and integration tests (`pytest`)
- [ ] Add `.env.example` for easier onboarding
- [ ] Implement a custom `500.html` error page
- [ ] Optimize static image assets (e.g., WebP compression)
- [ ] Complete the admin dashboard view (`app/templates/admin/dashboard.html`)

---

## License

This project is licensed under the MIT License — see the `LICENSE` file for details.
