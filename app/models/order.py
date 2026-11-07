from datetime import datetime, timezone

from sqlalchemy import Numeric

from app.extensions import db


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    order_number = db.Column(
        db.String(30),
        unique=True,
        nullable=False,
        index=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False,
        index=True,
    )

    status = db.Column(
        db.String(32),
        nullable=False,
        default="pending_review",
        server_default="pending_review",
        index=True,
    )

    payment_status = db.Column(
        db.String(20),
        nullable=False,
        default="unpaid",
        server_default="unpaid",
        index=True,
    )

    subtotal = db.Column(Numeric(12, 2), nullable=False)
    shipping_cost = db.Column(
        Numeric(12, 2),
        nullable=False,
        default=0,
    )
    discount_amount = db.Column(
        Numeric(12, 2),
        nullable=False,
        default=0,
    )
    total_amount = db.Column(Numeric(12, 2), nullable=False)

    recipient_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    shipping_address = db.Column(db.Text, nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    items = db.relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
    )

    user = db.relationship(
        "User",
        back_populates="orders",
    )

    def __repr__(self):
        return f"<Order {self.order_number}>"

    def __str__(self):
        return self.order_number