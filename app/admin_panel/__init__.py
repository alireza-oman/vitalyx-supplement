from app.admin_panel.views import (
    CategoryAdminView,
    OrderAdminView,
    PaymentAdminView,
    ProductAdminView,
    UserAdminView,
)
from app.extensions import admin, db
from app.models import Category, Order, Payment, Product, User


def setup_admin(app):
    admin.init_app(app)

    if len(admin._views) <= 1:
        admin.add_view(ProductAdminView(Product, db.session, name="Products"))
        admin.add_view(CategoryAdminView(Category, db.session, name="Categories"))
        admin.add_view(UserAdminView(User, db.session, name="Users"))
        admin.add_view(OrderAdminView(Order, db.session, name="Orders"))
        admin.add_view(PaymentAdminView(Payment, db.session, name="Payments"))