from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required, current_user

from app.models import Order


orders_bp = Blueprint(
    "orders",
    __name__,
    url_prefix="/orders"
)

@orders_bp.route("/my-order", methods=["GET", "POST"])
@login_required
def my_orders():
    orders = (
        Order.query
        .filter_by(user_id=current_user.id)
        .order_by(Order.created_at.desc())
        .all()
    )

    return render_template(
        "orders/my_orders.html",
        orders=orders
    )
@orders_bp.route("/<int:order_id>", methods=["GET"])
@login_required
def order_detail(order_id):
    user_order = Order.query.filter_by(
        id=order_id,
        user_id=current_user.id
    ).first()

    if user_order is None:
        flash("Order does not exist.", "danger")
        return redirect(url_for("checkout.checkout"))

    return render_template(
        "orders/order_detail.html",
        user_order=user_order,
        order_items=user_order.items
    )