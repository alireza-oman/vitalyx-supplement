import os
from pathlib import Path

from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    send_from_directory,
    url_for,
)
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError

from app.admin_panel.views import secure_image_name
from app.extensions import db
from app.forms import PaymentForm
from app.models import Order, Payment

payment_bp = Blueprint("payments", __name__, url_prefix="/payments")


@payment_bp.route("/submit-payment/<int:order_id>", methods=["GET", "POST"])
@login_required
def submit_payment(order_id):
    form = PaymentForm()

    # Verify order ownership
    user_order = Order.query.filter_by(
        id=order_id,
        user_id=current_user.id,
    ).first()

    if not user_order:
        flash("Order does not exist.", "danger")
        return redirect(url_for("orders.my_orders"))

    # Verify order status and payment status
    if user_order.status != "awaiting_payment" or user_order.payment_status == "paid":
        flash("This order is not awaiting payment.", "warning")
        return redirect(url_for("orders.order_detail", order_id=order_id))

    # Prevent duplicate receipt submissions while a payment is pending review
    pending_payment = Payment.query.filter_by(
        order_id=user_order.id,
        status="pending",
    ).first()

    if pending_payment:
        flash("Your payment receipt is already waiting for review.", "warning")
        return redirect(url_for("orders.order_detail", order_id=order_id))

    if form.validate_on_submit():
        tracking_number = form.tracking_number.data.strip()
        image = form.receipt_image.data

        # Generate a safe random filename
        filename = secure_image_name("", image)

        # Ensure the receipts upload directory exists
        upload_folder = Path(current_app.instance_path) / "receipts"
        upload_folder.mkdir(parents=True, exist_ok=True)

        image_path = upload_folder / filename

        # Save the uploaded receipt image
        try:
            image.save(image_path)
        except OSError:
            current_app.logger.exception("Receipt image save failed.")
            flash("Could not save the receipt image. Please try again.", "danger")
            return redirect(url_for("orders.order_detail", order_id=order_id))

        # Create the payment record
        payment = Payment(
            order_id=user_order.id,
            amount=user_order.total_amount,
            method="card_transfer",
            tracking_number=tracking_number,
            receipt_image=filename,
            status="pending",
        )

        # Save payment record to database
        try:
            db.session.add(payment)
            db.session.commit()
            flash("Payment receipt submitted successfully.", "success")
        except SQLAlchemyError:
            db.session.rollback()
            image_path.unlink(missing_ok=True)
            current_app.logger.exception("Payment submission failed.")
            flash("Could not submit payment. Please try again.", "danger")

        return redirect(url_for("orders.order_detail", order_id=order_id))

    return render_template(
        "payments/submit_payment.html",
        form=form,
        order=user_order,
    )


@payment_bp.route("/receipts/<path:filename>")
@login_required
def view_receipt(filename):
    if not current_user.is_admin:
        abort(403)

    safe_filename = os.path.basename(filename)
    upload_folder = Path(current_app.instance_path) / "receipts"

    return send_from_directory(upload_folder, safe_filename)