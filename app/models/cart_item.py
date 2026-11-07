from app.extensions import db

from sqlalchemy import CheckConstraint, UniqueConstraint


class CartItem(db.Model):
    __tablename__ = "cart_items"

    __table_args__ = (
        UniqueConstraint(
            "cart_id",
            "product_id",
            name="uq_cart_item_product",
        ),
        CheckConstraint(
            "quantity > 0",
            name="ck_cart_item_quantity_positive",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    cart_id = db.Column(
        db.Integer,
        db.ForeignKey("carts.id"),
        nullable=False,
        index=True,
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False,
        index=True,
    )

    quantity = db.Column(
        db.Integer,
        default=1,
        nullable=False,
    )

    cart = db.relationship(
        "Cart",
        back_populates="items",
    )

    product = db.relationship(
        "Product",
        back_populates="cart_items",
    )

    def __repr__(self):
        return f"<CartItem {self.id}>"