import uuid
from decimal import Decimal

from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.forms import CheckoutForm
from app.models import Cart, Order, OrderItem, Product

checkout_bp = Blueprint(
    "checkout",
    __name__,
    url_prefix="/checkout",
)


def generate_order_number():
    return f"VIT-{uuid.uuid4().hex[:12].upper()}"


@checkout_bp.route("/", methods=["GET"])
@login_required
def checkout():
    form = CheckoutForm()

    user_cart = Cart.query.filter_by(user_id=current_user.id).first()

    if user_cart is None or not user_cart.items:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("cart.all_cart"))

    cart_items = list(user_cart.items)

    subtotal = sum(
        (
            item.product.price * item.quantity
            for item in cart_items
            if item.product is not None
        ),
        Decimal("0.00"),
    )

    return render_template(
        "checkout/checkout.html",
        form=form,
        cart_items=cart_items,
        subtotal=subtotal,
    )


@checkout_bp.route("/place_order", methods=["POST"])
@login_required
def place_order():
    form = CheckoutForm()

    user_cart = Cart.query.filter_by(user_id=current_user.id).first()

    if user_cart is None or not user_cart.items:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("cart.all_cart"))

    cart_items = list(user_cart.items)

    subtotal = sum(
        (
            item.product.price * item.quantity
            for item in cart_items
            if item.product is not None
        ),
        Decimal("0.00"),
    )

    if form.validate_on_submit():
        recipient_name = form.recipient_name.data.strip()
        phone = form.phone.data.strip()
        postal_code = form.postal_code.data.strip()
        shipping_address = form.shipping_address.data.strip()

        try:
            # Recheck products and stock before creating the order.
            # Lock product rows in a consistent order where supported.
            products_by_item = {}

            for item in sorted(
                cart_items,
                key=lambda cart_item: cart_item.product_id or 0,
            ):
                product = (
                    Product.query
                    .filter_by(id=item.product_id)
                    .with_for_update()
                    .populate_existing()
                    .first()
                )

                if (
                    product is None
                    or not product.is_active
                    or product.stock < item.quantity
                ):
                    db.session.rollback()
                    flash(
                        "A product in your cart is unavailable "
                        "or has insufficient stock.",
                        "danger",
                    )
                    return redirect(url_for("cart.all_cart"))

                products_by_item[item.id] = product

            # Recalculate subtotal using current database prices.
            subtotal = sum(
                (
                    products_by_item[item.id].price * item.quantity
                    for item in cart_items
                ),
                Decimal("0.00"),
            )

            shipping_cost = Decimal("0.00")
            discount_amount = Decimal("0.00")
            total_amount = subtotal + shipping_cost - discount_amount

            # Create the order.
            order = Order(
                order_number=generate_order_number(),
                user_id=current_user.id,
                status="pending_review",
                payment_status="unpaid",
                subtotal=subtotal,
                shipping_cost=shipping_cost,
                discount_amount=discount_amount,
                total_amount=total_amount,
                recipient_name=recipient_name,
                phone=phone,
                postal_code=postal_code,
                shipping_address=shipping_address,
            )

            db.session.add(order)
            db.session.flush()

            # Create order items and decrease product stock.
            for item in cart_items:
                product = products_by_item[item.id]

                order_item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    product_name=product.name,
                    unit_price=product.price,
                    quantity=item.quantity,
                    line_total=product.price * item.quantity,
                )

                db.session.add(order_item)
                product.stock -= item.quantity

            # Remove purchased items from the cart.
            for item in cart_items:
                db.session.delete(item)

            db.session.commit()

        except SQLAlchemyError:
            db.session.rollback()
            current_app.logger.exception("Failed to place an order.")
            flash(
                "We couldn't place your order. Please try again.",
                "danger",
            )
            return redirect(url_for("checkout.checkout"))

        flash("Your order has been placed and is now pending review.", "success")
        return redirect(url_for("orders.order_detail", order_id=order.id))

    return render_template(
        "checkout/checkout.html",
        form=form,
        cart_items=cart_items,
        subtotal=subtotal,
    )