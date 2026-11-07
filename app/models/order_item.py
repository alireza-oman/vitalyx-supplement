from sqlalchemy import CheckConstraint, Numeric

from app.extensions import db


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id"),
        nullable=False,
        index=True,
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=True,
    )

    # Snapshot of the product at purchase time
    product_name = db.Column(db.String(150), nullable=False)

    unit_price = db.Column(Numeric(12, 2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    line_total = db.Column(Numeric(12, 2), nullable=False)

    order = db.relationship(
        "Order",
        back_populates="items",
    )

    product = db.relationship("Product")

    __table_args__ = (
        CheckConstraint(
            "quantity > 0",
            name="check_order_item_quantity_positive",
        ),
    )

    def __repr__(self):
        return f"<OrderItem {self.product_name} x{self.quantity}>"