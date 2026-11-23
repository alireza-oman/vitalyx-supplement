from decimal import Decimal
from flask import redirect, request, url_for
from flask_admin import Admin, AdminIndexView, expose
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import func

db = SQLAlchemy()
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address)
csrf = CSRFProtect()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "info"


class StrictAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return (
            current_user.is_authenticated
            and getattr(current_user, "is_admin", False)
        )

    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login", next=request.url))
        return redirect(url_for("main.home"))

    @expose("/")
    def index(self):
        from app.models import Order, Payment, Product, User

        # KPI Metrics
        total_revenue = (
            db.session.query(func.coalesce(func.sum(Order.total_amount), 0))
            .filter(Order.payment_status == "paid")
            .scalar()
        ) or Decimal("0.00")

        total_orders = Order.query.count()
        pending_orders = Order.query.filter(
            Order.status.in_(["pending_review", "pending"])
        ).count()

        pending_payments_count = Payment.query.filter_by(status="pending").count()
        total_products = Product.query.count()
        total_users = User.query.count()

        # Tables Data
        recent_orders = (
            Order.query.order_by(Order.created_at.desc()).limit(6).all()
        )
        pending_payments = (
            Payment.query.filter_by(status="pending")
            .order_by(Payment.created_at.desc())
            .limit(5)
            .all()
        )
        low_stock_products = (
            Product.query.filter(Product.stock <= 5)
            .order_by(Product.stock.asc())
            .limit(5)
            .all()
        )

        return self.render(
            "admin/dashboard.html",
            total_revenue=total_revenue,
            total_orders=total_orders,
            pending_orders=pending_orders,
            pending_payments_count=pending_payments_count,
            total_products=total_products,
            total_users=total_users,
            recent_orders=recent_orders,
            pending_payments=pending_payments,
            low_stock_products=low_stock_products,
        )


admin = Admin(
    name="VITALYX Admin",
    index_view=StrictAdminIndexView(name="Dashboard", url="/admin"),
)

admin.base_template = "admin/master.html"