[English](#vitalyx-supplement) | [فارسی](#vitalyx-supplement-persian)

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
- **Admin Panel:** Administrative interface built with `Flask-Admin` featuring a custom metrics dashboard and management views for orders, payments, products, categories, and users.
- **Rate Limiting & Form Protection:** Request throttling via `Flask-Limiter` and CSRF protection via `Flask-WTF`.
- **Custom Error Pages:** Styled error templates for HTTP `403`, `404`, and `502` responses.
- **Database Migrations:** Version-controlled schema evolution managed via Alembic (`Flask-Migrate`).

---

## Application Flow

1. **Customer Journey:** Browse catalog → View product details → Add to cart → Proceed to checkout → Submit payment proof → Track order status.
2. **Admin Journey:** Access admin panel → Review dashboard metrics, incoming orders & submitted payments → Approve/reject payments and update order statuses.

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
   git clone [https://github.com/alireza-oman/vitalyx-supplement.git](https://github.com/alireza-oman/vitalyx-supplement.git)
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

- [x] Complete the admin dashboard view (`app/templates/admin/dashboard.html`)
- [ ] Add automated unit and integration tests (`pytest`)
- [ ] Add `.env.example` for easier onboarding
- [ ] Implement a custom `500.html` error page
- [ ] Optimize static image assets (e.g., WebP compression)

---

## License

This project is licensed under the MIT License — see the `LICENSE` file for details.

---

<div id="vitalyx-supplement-persian" dir="rtl">

# فروشگاه مکمل‌های ورزشی Vitalyx

یک وب‌اپلیکیشن فروشگاهی ماژولار ساخته‌شده با **Python** و **Flask** برای مدیریت و فروش مکمل‌های ورزشی و سلامتی. این پروژه شامل احراز هویت کاربران، سبد خرید متصل به دیتابیس، فرآیند ثبت سفارش و پیگیری آن، ثبت و بررسی دستی رسید پرداخت، و یک پنل مدیریت اختصاصی است.

---

## ویژگی‌ها

- **کاتالوگ محصولات:** دسته‌بندی مکمل‌ها و صفحه جزئیات کامل برای هر محصول.
- **احراز هویت کاربران:** ثبت‌نام و ورود امن با `Flask-Login` و `Flask-WTF`.
- **سبد خرید ماندگار:** افزودن، ویرایش تعداد و حذف محصولات به‌صورت مستقیم در دیتابیس.
- **ثبت و پیگیری سفارش:** تکمیل خرید، ثبت سفارش و مشاهده تاریخچه و وضعیت سفارش‌ها.
- **فرآیند پرداخت دستی:** امکان ثبت اطلاعات و رسید پرداخت توسط مشتری و بررسی/تایید آن توسط ادمین.
- **پنل مدیریت اختصاصی:** داشبورد آماری و مدیریت سفارش‌ها، پرداخت‌ها، محصولات، دسته‌بندی‌ها و کاربران با `Flask-Admin`.
- **امنیت و محدودیت درخواست:** محافظت در برابر CSRF با `Flask-WTF` و محدودسازی نرخ درخواست‌ها با `Flask-Limiter`.
- **صفحات خطای اختصاصی:** قالب‌های طراحی‌شده برای خطاهای `403`، `404` و `502`.
- **مدیریت تغییرات دیتابیس:** مایگریشن‌های نسخه‌بندی‌شده با `Alembic` (`Flask-Migrate`).

---

## جریان کار سیستم

1. **مسیر مشتری:** مشاهده محصولات ← بررسی جزئیات ← افزودن به سبد خرید ← تکمیل فرم سفارش ← ثبت رسید پرداخت ← پیگیری وضعیت سفارش.
2. **مسیر ادمین:** ورود به پنل مدیریت ← بررسی آمار داشبورد و سفارش‌های جدید ← تایید یا رد رسیدهای پرداخت و به‌روزرسانی وضعیت ارسال.

---

## تکنولوژی‌های استفاده‌شده

- **بک‌اند:** Python, Flask, Flask-Login, Flask-Admin, Flask-Limiter
- **دیتابیس و ORM:** SQLAlchemy, Alembic (Flask-Migrate)
- **فرم‌ها و اعتبارسنجی:** Flask-WTF, WTForms
- **فرانت‌اند:** Jinja2 Templates, HTML5, CSS3, Vanilla JavaScript

---

## راهنمای نصب و اجرا

### پیش‌نیازها

- پایتون نسخه `3.10` یا بالاتر
- `pip` و `venv`

### مراحل راه‌اندازی

1. **کلون کردن پروژه:**

<div dir="ltr">

```bash
git clone [https://github.com/alireza-oman/vitalyx-supplement.git](https://github.com/alireza-oman/vitalyx-supplement.git)
cd vitalyx-supplement
```

</div>

2. **ساخت و فعال‌سازی محیط مجازی:**

<div dir="ltr">

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

</div>

3. **نصب وابستگی‌ها:**

<div dir="ltr">

```bash
pip install -r requirements.txt
```

</div>

4. **تنظیم متغیرهای محیطی:**
   یک فایل با نام `.env` در ریشه پروژه بسازید و مقادیر زیر را در آن قرار دهید:

<div dir="ltr">

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
APP_ENV=development
```

</div>

   > **نکته امنیتی:** هرگز فایل `.env` یا کلیدهای واقعی خود را روی گیت کامیت نکنید.

5. **اجرای مایگریشن‌های دیتابیس:**

<div dir="ltr">

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

</div>

6. **اجرای برنامه:**

<div dir="ltr">

```bash
python run.py
```

</div>

   برنامه روی آدرس `http://127.0.0.1:5000` در دسترس خواهد بود.

---

## نقشه راه و بهبودهای آینده

- [x] تکمیل داشبورد پنل ادمین (`app/templates/admin/dashboard.html`)
- [ ] افزودن تست‌های خودکار با `pytest`
- [ ] افزودن فایل `.env.example` برای راه‌اندازی سریع‌تر
- [ ] طراحی صفحه خطای اختصاصی `500.html`
- [ ] بهینه‌سازی حجم تصاویر استاتیک (تبدیل به WebP)

---

## لایسنس

این پروژه تحت لایسنس **MIT** منتشر شده است — برای جزئیات بیشتر فایل `LICENSE` را مشاهده کنید.

</div>
