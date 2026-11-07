import os
from flask import Flask, render_template
from flask_login import current_user

from app.admin_panel.views import (
    CategoryAdminView,
    OrderAdminView,
    PaymentAdminView,
    ProductAdminView,
    SecureModelView,
)
from app.config import DevConfig, config_options
from app.extensions import admin, csrf, db, limiter, login_manager, migrate
from app.models import (
    Cart,
    CartItem,
    Category,
    Order,
    OrderItem,
    Payment,
    Product,
    User,
)
from app.routes import (
    auth_bp,
    cart_bp,
    checkout_bp,
    main_bp,
    orders_bp,
    payment_bp,
)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def create_app():
    app = Flask(__name__)

    # Load application configuration
    config_name = os.environ.get("APP_ENV", "development")
    app.config.from_object(config_options.get(config_name, DevConfig))

    # Register error handlers
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(500)
    def internal_server_error(error):
        db.session.rollback()
        return render_template("errors/502.html"), 500

    @app.errorhandler(502)
    def bad_gateway(error):
        return render_template("errors/502.html"), 502

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    limiter.init_app(app)
    csrf.init_app(app)

    # Initialize Flask-Admin
    admin.init_app(app)

    # Prevent duplicate admin views from being registered
    if len(admin._views) <= 1:
        admin.add_view(ProductAdminView(Product, db.session, name="Products"))
        admin.add_view(CategoryAdminView(Category, db.session, name="Categories"))
        admin.add_view(SecureModelView(User, db.session, name="Users"))
        admin.add_view(OrderAdminView(Order, db.session, name="Orders"))
        admin.add_view(PaymentAdminView(Payment, db.session, name="Payments"))

    # Register application blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(checkout_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(payment_bp)

    @app.context_processor
    def inject_cart_count():
        cart_count = 0

        if current_user.is_authenticated:
            user_cart = Cart.query.filter_by(user_id=current_user.id).first()

            if user_cart:
                cart_count = sum(item.quantity for item in user_cart.items)

        return {"cart_count": cart_count}

    return app