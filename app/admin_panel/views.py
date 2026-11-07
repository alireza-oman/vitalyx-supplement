import datetime
import os
import uuid

from flask import current_app, flash, redirect, request, url_for
from flask_admin import expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import ImageUploadField
from flask_login import current_user
from flask_wtf.csrf import generate_csrf
from markupsafe import Markup, escape
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename
from wtforms import TextAreaField

from app.extensions import db
from app.models import Order, Payment, Product


# -------------------------------------------------------------------
# Upload settings
# -------------------------------------------------------------------

PRODUCT_UPLOAD_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "static",
        "uploads",
        "products",
    )
)

os.makedirs(PRODUCT_UPLOAD_PATH, exist_ok=True)


def secure_image_name(obj, file_data):
    """Create a random filename while keeping the original extension."""
    original_name = secure_filename(file_data.filename or "")
    extension = os.path.splitext(original_name)[1].lower()

    return f"{uuid.uuid4().hex}{extension}"


# -------------------------------------------------------------------
# Shared admin view
# -------------------------------------------------------------------

class SecureModelView(ModelView):
    """Only authenticated admin users can access these views."""

    page_size = 20

    def is_accessible(self):
        return (
            current_user.is_authenticated
            and getattr(current_user, "is_admin", False)
        )

    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("auth.login", next=request.url))

        return redirect(url_for("main.home"))


# -------------------------------------------------------------------
# User
# -------------------------------------------------------------------

class UserAdminView(SecureModelView):
    can_create = False
    can_view_details = True

    column_list = ["id", "username", "email", "is_admin", "created_at"]
    column_searchable_list = ["username", "email"]
    column_filters = ["is_admin", "created_at"]
    column_editable_list = ["is_admin"]
    column_exclude_list = ["password_hash"]
    form_columns = ["username", "email", "is_admin"]
    column_default_sort = ("created_at", True)


# -------------------------------------------------------------------
# Category
# -------------------------------------------------------------------

class CategoryAdminView(SecureModelView):
    column_list = ["name", "slug", "is_active", "created_at"]

    column_editable_list = ["name", "is_active"]
    column_searchable_list = ["name", "slug"]
    column_filters = ["is_active"]

    form_columns = ["name", "slug", "description", "is_active"]
    form_overrides = {"description": TextAreaField}


# -------------------------------------------------------------------
# Product
# -------------------------------------------------------------------

def format_product_image(view, context, product, name):
    """Show a small product image in the admin table."""

    if product.image and product.image.startswith(("http://", "https://")):
        image_url = product.image

    elif product.image:
        filename = os.path.basename(product.image)
        image_url = url_for(
            "static",
            filename=f"uploads/products/{filename}",
        )

    else:
        image_url = url_for(
            "static",
            filename="images/products/default-product.png",
        )

    return Markup(
        '<img src="{}" alt="Product" '
        'style="width:44px;height:44px;object-fit:cover;border-radius:7px;">'
    ).format(escape(image_url))


class ProductAdminView(SecureModelView):
    column_list = [
        "image",
        "name",
        "brand",
        "category",
        "price",
        "stock",
        "is_active",
    ]

    column_formatters = {
        "image": format_product_image,
    }

    column_editable_list = ["price", "stock", "is_active"]
    column_searchable_list = ["name", "slug", "brand"]
    column_filters = ["is_active", "brand", "price", "stock", "category"]

    form_columns = [
        "name",
        "slug",
        "brand",
        "category",
        "price",
        "stock",
        "image",
        "description",
        "is_active",
    ]

    form_overrides = {
        "description": TextAreaField,
        "image": ImageUploadField,
    }

    form_args = {
        "image": {
            "label": "Product Image",
            "base_path": PRODUCT_UPLOAD_PATH,
            "url_relative_path": "uploads/products/",
            "allowed_extensions": ["jpg", "jpeg", "png", "webp"],
            "namegen": secure_image_name,
        }
    }

    form_widget_args = {
        "description": {"rows": 4},
        "slug": {"placeholder": "e.g. vitalyx-iso-whey"},
    }

    column_default_sort = ("created_at", True)


# -------------------------------------------------------------------
# Order formatting helpers
# -------------------------------------------------------------------

def format_order_customer(view, context, order, name):
    if not order.user:
        return "Unknown Customer"

    return Markup("{} ({})").format(
        escape(order.user.username),
        escape(order.user.email),
    )


def format_order_items(view, context, order, name):
    """Show the ordered products and their prices on the order details page."""

    if not order.items:
        return "No items found."

    rows = []

    for item in order.items:
        rows.append(
            Markup(
                """
                <div style="margin-bottom:12px;padding-bottom:10px;
                            border-bottom:1px solid var(--adm-border, #e8e8e8);">
                    <strong>{}</strong>
                    <div>Quantity: {}</div>
                    <div>Unit price: ${:,.2f}</div>
                    <div>Line total: ${:,.2f}</div>
                </div>
                """
            ).format(
                escape(item.product_name),
                item.quantity,
                item.unit_price,
                item.line_total,
            )
        )

    return Markup("").join(rows)


# -------------------------------------------------------------------
# Order
# -------------------------------------------------------------------

class OrderAdminView(SecureModelView):
    details_template = "admin/orders/details.html"

    # Orders are created by customers, not by admins in this screen.
    can_create = False
    can_edit = False
    can_delete = False
    can_view_details = True

    column_list = [
        "order_number",
        "user",
        "status",
        "payment_status",
        "total_amount",
        "created_at",
    ]

    column_labels = {
        "order_number": "Order Number",
        "user": "Customer",
        "status": "Order Status",
        "payment_status": "Payment Status",
        "total_amount": "Total Amount",
        "created_at": "Created At",
    }

    column_formatters = {
        "user": format_order_customer,
    }

    column_searchable_list = [
        "order_number",
        "status",
        "payment_status",
    ]

    column_filters = [
        "status",
        "payment_status",
        "created_at",
    ]

    column_sortable_list = [
        "order_number",
        "status",
        "payment_status",
        "total_amount",
        "created_at",
    ]

    column_details_list = [
        "id",
        "user",
        "order_number",
        "status",
        "payment_status",
        "subtotal",
        "shipping_cost",
        "discount_amount",
        "total_amount",
        "recipient_name",
        "phone",
        "shipping_address",
        "postal_code",
        "created_at",
        "updated_at",
        "items",
    ]

    column_formatters_detail = {
        "user": format_order_customer,
        "items": format_order_items,
    }

    column_default_sort = ("created_at", True)

    def _get_order(self, order_id):
        """Load an order with row-level locking where supported."""
        return (
            Order.query
            .filter_by(id=order_id)
            .with_for_update()
            .populate_existing()
            .first()
        )

    def _order_details_url(self, order_id):
        return self.get_url(".details_view", id=order_id)

    def _show_order_not_found(self):
        flash("Order not found.", "danger")
        return redirect(self.get_url(".index_view"))

    def _show_database_error(self, message, order_id):
        db.session.rollback()

        current_app.logger.exception(
            "Order admin action failed for order %s.",
            order_id,
        )

        flash(message, "danger")
        return redirect(self._order_details_url(order_id))

    @expose("/approve/<int:order_id>/", methods=("POST",))
    def approve_order(self, order_id):
        if not self.is_accessible():
            return self.inaccessible_callback("approve_order")

        order = self._get_order(order_id)

        if order is None:
            return self._show_order_not_found()

        if order.status not in {"pending_review", "pending"}:
            flash("This order is not waiting for review.", "warning")
            return redirect(self._order_details_url(order_id))

        if order.payment_status == "paid":
            flash("This order has already been paid.", "warning")
            return redirect(self._order_details_url(order_id))

        try:
            order.status = "awaiting_payment"
            db.session.commit()

            flash("Order approved. It is now awaiting payment.", "success")

        except SQLAlchemyError:
            return self._show_database_error(
                "Could not approve this order. Please try again.",
                order_id,
            )

        return redirect(self._order_details_url(order_id))

    @expose("/reject/<int:order_id>/", methods=("POST",))
    def reject_order(self, order_id):
        if not self.is_accessible():
            return self.inaccessible_callback("reject_order")

        order = self._get_order(order_id)

        if order is None:
            return self._show_order_not_found()

        allowed_statuses = {
            "pending_review",
            "pending",
            "awaiting_payment",
        }

        if order.status not in allowed_statuses:
            flash("This order cannot be rejected in its current status.", "warning")
            return redirect(self._order_details_url(order_id))

        if order.payment_status == "paid":
            flash("A paid order cannot be rejected here.", "warning")
            return redirect(self._order_details_url(order_id))

        try:
            items = sorted(
                order.items,
                key=lambda item: item.product_id or 0,
            )

            for item in items:
                if item.product_id is None:
                    continue

                product = (
                    Product.query
                    .filter_by(id=item.product_id)
                    .with_for_update()
                    .populate_existing()
                    .first()
                )

                if product is not None:
                    product.stock += item.quantity

            order.status = "rejected"
            db.session.commit()

            flash("Order rejected. Product stock has been restored.", "success")

        except SQLAlchemyError:
            return self._show_database_error(
                "Could not reject this order. Please try again.",
                order_id,
            )

        return redirect(self._order_details_url(order_id))

    @expose("/revoke-approval/<int:order_id>/", methods=("POST",))
    def revoke_approval(self, order_id):
        if not self.is_accessible():
            return self.inaccessible_callback("revoke_approval")

        order = self._get_order(order_id)

        if order is None:
            return self._show_order_not_found()

        can_revoke = (
            order.status == "awaiting_payment"
            and order.payment_status == "unpaid"
        )

        if not can_revoke:
            flash("This order's approval cannot be revoked.", "warning")
            return redirect(self._order_details_url(order_id))

        try:
            order.status = "pending_review"
            db.session.commit()

            flash(
                "Approval revoked. The order is waiting for review again.",
                "success",
            )

        except SQLAlchemyError:
            return self._show_database_error(
                "Could not revoke the order approval.",
                order_id,
            )

        return redirect(self._order_details_url(order_id))

    @expose("/ship/<int:order_id>/", methods=("POST",))
    def ship_order(self, order_id):
        if not self.is_accessible():
            return self.inaccessible_callback("ship_order")

        order = self._get_order(order_id)

        if order is None:
            return self._show_order_not_found()

        if order.status != "processing" or order.payment_status != "paid":
            flash("Only paid orders in 'processing' status can be shipped.", "warning")
            return redirect(self._order_details_url(order_id))

        try:
            order.status = "shipped"
            db.session.commit()
            flash("Order has been marked as shipped.", "success")
        except SQLAlchemyError:
            return self._show_database_error(
                "Could not mark order as shipped.",
                order_id,
            )

        return redirect(self._order_details_url(order_id))

    @expose("/deliver/<int:order_id>/", methods=("POST",))
    def deliver_order(self, order_id):
        if not self.is_accessible():
            return self.inaccessible_callback("deliver_order")

        order = self._get_order(order_id)

        if order is None:
            return self._show_order_not_found()

        if order.status != "shipped":
            flash("Only shipped orders can be marked as delivered.", "warning")
            return redirect(self._order_details_url(order_id))

        try:
            order.status = "delivered"
            db.session.commit()
            flash("Order has been marked as delivered.", "success")
        except SQLAlchemyError:
            return self._show_database_error(
                "Could not mark order as delivered.",
                order_id,
            )

        return redirect(self._order_details_url(order_id))


# -------------------------------------------------------------------
# Payment formatting helpers
# -------------------------------------------------------------------

def format_payment_order(view, context, payment, name):
    if payment.order:
        order_url = url_for("order.details_view", id=payment.order.id)
        return Markup('<a href="{}" class="payment-order-number">{}</a>').format(
            escape(order_url),
            escape(payment.order.order_number),
        )

    return f"Order #{payment.order_id}"


def get_payment_receipt_url(payment):
    if not payment.receipt_image:
        return None

    image = str(payment.receipt_image).strip().replace("\\", "/")
    filename = os.path.basename(image)

    if not filename:
        return None

    return url_for("payments.view_receipt", filename=filename)


def format_payment_receipt(view, context, payment, name):
    image_url = get_payment_receipt_url(payment)

    if not image_url:
        return "No receipt"

    return Markup(
        """
        <a href="{}" target="_blank" rel="noopener noreferrer">
            <img src="{}" alt="Payment receipt"
                 style="width:58px;height:48px;object-fit:cover;
                        border-radius:7px;border:1px solid var(--adm-border, #e8e5ef);">
        </a>
        """
    ).format(
        escape(image_url),
        escape(image_url),
    )


def format_payment_receipt_detail(view, context, payment, name):
    image_url = get_payment_receipt_url(payment)

    if not image_url:
        return "No receipt uploaded."

    return Markup(
        """
        <a href="{}" target="_blank" rel="noopener noreferrer">
            <img src="{}" alt="Payment receipt"
                 style="display:block;width:100%;max-width:420px;
                        max-height:520px;object-fit:contain;
                        border:1px solid var(--adm-border, #e8e5ef);border-radius:10px;">
        </a>
        <p style="color:var(--adm-text-muted, #858398);font-size:12px;margin-top:8px;">
            Click the image to open the original file.
        </p>
        """
    ).format(
        escape(image_url),
        escape(image_url),
    )


def format_payment_status(view, context, payment, name):
    status = (payment.status or "unknown").lower()

    status_labels = {
        "pending": ("Pending Review", "pending"),
        "approved": ("Approved", "approved"),
        "rejected": ("Rejected", "rejected"),
    }

    label, css_class = status_labels.get(
        status,
        (status.replace("_", " ").title(), "unknown"),
    )

    approve_url = url_for(
        f"{view.endpoint}.approve_payment",
        payment_id=payment.id,
    )

    reject_url = url_for(
        f"{view.endpoint}.reject_payment",
        payment_id=payment.id,
    )

    csrf_token = generate_csrf()

    badge = Markup(
        '<span class="payment-status payment-status--{}">{}</span>'
    ).format(
        css_class,
        escape(label),
    )

    buttons = []

    if status != "approved":
        buttons.append(
            Markup(
                """
                <form method="POST" action="{}">
                    <input type="hidden" name="csrf_token" value="{}">
                    <button type="submit"
                        style="background:#16a34a;color:white;border:0;
                        padding:6px 12px;border-radius:6px;cursor:pointer;font-weight:600;font-size:12px;">
                        Approve
                    </button>
                </form>
                """
            ).format(approve_url, csrf_token)
        )

    if status != "rejected":
        buttons.append(
            Markup(
                """
                <form method="POST" action="{}">
                    <input type="hidden" name="csrf_token" value="{}">
                    <button type="submit"
                        style="background:#dc2626;color:white;border:0;
                        padding:6px 12px;border-radius:6px;cursor:pointer;font-weight:600;font-size:12px;">
                        Reject
                    </button>
                </form>
                """
            ).format(reject_url, csrf_token)
        )

    actions = Markup(
        '<div style="display:flex; gap:6px; margin-top:8px; flex-wrap:wrap;">{}</div>'
    ).format(Markup("").join(buttons))

    return badge + actions


# -------------------------------------------------------------------
# Payment
# -------------------------------------------------------------------

class PaymentAdminView(SecureModelView):
    list_template = "admin/payments/list.html"
    details_template = "admin/payments/details.html"

    # Customers submit payments; admins review them.
    can_create = False
    can_edit = False
    can_delete = True
    can_view_details = True

    column_list = [
        "id",
        "order",
        "amount",
        "method",
        "tracking_number",
        "receipt_image",
        "status",
        "reviewed_at",
    ]

    column_labels = {
        "id": "Payment ID",
        "order": "Order Number",
        "amount": "Amount",
        "method": "Payment Method",
        "tracking_number": "Tracking Number",
        "receipt_image": "Receipt",
        "status": "Payment Status",
        "reviewed_at": "Reviewed At",
    }

    column_formatters = {
        "order": format_payment_order,
        "receipt_image": format_payment_receipt,
        "status": format_payment_status,
    }

    column_details_list = [
        "id",
        "order",
        "amount",
        "method",
        "tracking_number",
        "receipt_image",
        "status",
        "created_at",
        "reviewed_at",
    ]

    column_formatters_detail = {
        "order": format_payment_order,
        "receipt_image": format_payment_receipt_detail,
        "status": format_payment_status,
    }

    column_searchable_list = [
        "tracking_number",
        "status",
        "method",
    ]

    column_filters = [
        "status",
        "method",
        "reviewed_at",
    ]

    column_sortable_list = [
        "id",
        "amount",
        "status",
        "reviewed_at",
    ]

    column_default_sort = ("id", True)

    def _redirect_after_action(self):
        if request.referrer:
            return redirect(request.referrer)
        return redirect(self.get_url(".index_view"))

    def _change_payment_status(self, payment_id, new_status):
        if not self.is_accessible():
            return self.inaccessible_callback("payment_action")

        payment = (
            Payment.query
            .filter_by(id=payment_id)
            .with_for_update()
            .populate_existing()
            .first()
        )

        if not payment:
            flash("Payment not found.", "danger")
            return self._redirect_after_action()

        order = payment.order

        if not order:
            flash("Related order not found.", "danger")
            return self._redirect_after_action()

        if new_status == "approved" and order.status == "rejected":
            flash("Cannot approve payment for a rejected order.", "warning")
            return self._redirect_after_action()

        if new_status == "rejected" and order.status in {"shipped", "delivered"}:
            flash("Cannot reject a payment after shipment.", "warning")
            return self._redirect_after_action()

        try:
            payment.status = new_status
            payment.reviewed_at = datetime.datetime.now(datetime.timezone.utc)

            db.session.flush()

            approved_payment = Payment.query.filter_by(
                order_id=order.id,
                status="approved",
            ).first()

            if approved_payment:
                order.payment_status = "paid"

                if order.status == "awaiting_payment":
                    order.status = "processing"
            else:
                order.payment_status = "unpaid"

                if order.status == "processing":
                    order.status = "awaiting_payment"

            db.session.commit()

            flash(f"Payment successfully marked as {new_status}.", "success")

        except SQLAlchemyError:
            db.session.rollback()
            current_app.logger.exception(
                "Payment status update failed. Payment ID: %s",
                payment_id,
            )
            flash("Could not update payment status.", "danger")

        return self._redirect_after_action()

    @expose("/approve/<int:payment_id>/", methods=("POST",))
    def approve_payment(self, payment_id):
        return self._change_payment_status(payment_id, "approved")

    @expose("/reject/<int:payment_id>/", methods=("POST",))
    def reject_payment(self, payment_id):
        return self._change_payment_status(payment_id, "rejected")