from urllib.parse import urlparse

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models import Cart, CartItem, Product

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")


def _redirect_back(fallback_endpoint, **kwargs):
    """Redirect back to the referring page if it belongs to the same host."""
    referrer = request.referrer
    if referrer:
        parsed_ref = urlparse(referrer)
        if not parsed_ref.netloc or parsed_ref.netloc == request.host:
            return redirect(referrer)
    return redirect(url_for(fallback_endpoint, **kwargs))


# Display the user's shopping cart
@cart_bp.route("/all")
@login_required
def all_cart():
    user_cart = Cart.query.filter_by(user_id=current_user.id).first()
    cart_items = user_cart.items if user_cart else []

    return render_template(
        "cart/cart.html",
        cart_items=cart_items,
    )


# Add a product to the shopping cart
@cart_bp.route("/add/<int:product_id>", methods=["POST"])
@login_required
def add_cart(product_id):
    product = Product.query.get_or_404(product_id)

    if not product.is_active:
        flash("This product is not available.", "danger")
        return redirect(url_for("main.home"))

    if product.stock <= 0:
        flash("This product is out of stock.", "danger")
        return _redirect_back("main.product_detail", slug=product.slug)

    quantity_input = request.form.get("quantity")

    if not quantity_input:
        quantity = 1
    else:
        try:
            quantity = int(quantity_input)
        except (ValueError, TypeError):
            flash("Please enter a valid quantity.", "danger")
            return _redirect_back("main.product_detail", slug=product.slug)

    if quantity < 1:
        flash("Quantity must be at least 1.", "danger")
        return _redirect_back("main.product_detail", slug=product.slug)

    if quantity > product.stock:
        flash("Not enough stock available.", "danger")
        return _redirect_back("main.product_detail", slug=product.slug)

    try:
        user_cart = Cart.query.filter_by(user_id=current_user.id).first()

        if user_cart is None:
            user_cart = Cart(user_id=current_user.id)
            db.session.add(user_cart)
            db.session.flush()

        cart_item = CartItem.query.filter_by(
            cart_id=user_cart.id,
            product_id=product.id,
        ).first()

        new_quantity = (cart_item.quantity + quantity) if cart_item else quantity

        if new_quantity > product.stock:
            flash("Not enough stock available for the total quantity in your cart.", "danger")
            return _redirect_back("main.product_detail", slug=product.slug)

        if cart_item:
            cart_item.quantity = new_quantity
        else:
            cart_item = CartItem(
                cart_id=user_cart.id,
                product_id=product.id,
                quantity=quantity,
            )
            db.session.add(cart_item)

        db.session.commit()
        flash("Product added to your cart.", "success")

    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception("Failed to add product to cart.")
        flash("Could not add product to cart. Please try again.", "danger")

    return _redirect_back("main.product_detail", slug=product.slug)


# Update the quantity of an existing cart item
@cart_bp.route("/update_quantity/<int:item_id>", methods=["POST"])
@login_required
def update_quantity(item_id):
    user_cart = Cart.query.filter_by(user_id=current_user.id).first()

    if user_cart is None:
        flash("You don't have an active cart.", "danger")
        return redirect(url_for("cart.all_cart"))

    cart_item = CartItem.query.filter_by(
        id=item_id,
        cart_id=user_cart.id,
    ).first()

    if cart_item is None:
        flash("Item not found.", "danger")
        return redirect(url_for("cart.all_cart"))

    new_quantity = request.form.get("quantity", type=int)

    if new_quantity is None or new_quantity < 1:
        flash("Please enter a valid quantity.", "danger")
        return redirect(url_for("cart.all_cart"))

    product = cart_item.product

    if product is None or not product.is_active or product.stock <= 0:
        flash("This product is currently unavailable.", "danger")
        return redirect(url_for("cart.all_cart"))

    if new_quantity > product.stock:
        flash(f"Only {product.stock} units are available in stock.", "danger")
        return redirect(url_for("cart.all_cart"))

    try:
        cart_item.quantity = new_quantity
        db.session.commit()
        flash("Product quantity updated successfully.", "success")
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception("Failed to update cart item quantity.")
        flash("Could not update quantity. Please try again.", "danger")

    return redirect(url_for("cart.all_cart"))


# Remove an item from the shopping cart
@cart_bp.route("/delete/<int:item_id>", methods=["POST"])
@login_required
def delete_cart(item_id):
    user_cart = Cart.query.filter_by(user_id=current_user.id).first()

    if user_cart is None:
        flash("Your cart was not found.", "danger")
        return redirect(url_for("cart.all_cart"))

    cart_item = CartItem.query.filter_by(
        id=item_id,
        cart_id=user_cart.id,
    ).first()

    if cart_item is None:
        flash("Item not found in your cart.", "danger")
        return redirect(url_for("cart.all_cart"))

    try:
        db.session.delete(cart_item)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception("Failed to delete cart item.")
        flash("Could not remove the item. Please try again.", "danger")
        return redirect(url_for("cart.all_cart"))

    flash("Item removed successfully.", "success")
    return redirect(url_for("cart.all_cart"))