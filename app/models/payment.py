from datetime import datetime, timezone

from app.extensions import db


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id"),
        nullable=False,
        index=True,
    )

    amount = db.Column(db.Numeric(12, 2), nullable=False)
    method = db.Column(db.String(30), default="card_transfer", nullable=False)
    tracking_number = db.Column(db.String(100), nullable=False)
    receipt_image = db.Column(db.String(255), nullable=False)

    # Payment review status: pending, approved, rejected
    status = db.Column(
        db.String(20),
        default="pending",
        nullable=False,
        index=True,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    reviewed_at = db.Column(db.DateTime(timezone=True), nullable=True)

    order = db.relationship("Order", backref="payments")

    def __repr__(self):
        return f"<Payment #{self.id} for Order #{self.order_id} ({self.status})>"