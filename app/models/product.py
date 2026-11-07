from datetime import datetime, timezone

from sqlalchemy import CheckConstraint

from app.extensions import db


class Product(db.Model):
    __tablename__ = "products"

    __table_args__ = (
        CheckConstraint("price >= 0", name="ck_product_price_non_negative"),
        CheckConstraint("stock >= 0", name="ck_product_stock_non_negative"),
    )

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)
    slug = db.Column(db.String(180), unique=True, index=True, nullable=False)

    description = db.Column(db.Text, nullable=False)

    price = db.Column(db.Numeric(12, 2), nullable=False)
    stock = db.Column(db.Integer, default=0, nullable=False)

    image = db.Column(db.String(255), nullable=True)
    brand = db.Column(db.String(100), nullable=False)

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=False,
        index=True,
    )

    cart_items = db.relationship(
        "CartItem",
        back_populates="product",
        cascade="all, delete-orphan",
    )

    is_active = db.Column(db.Boolean, default=True, nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self):
        return f"<Product {self.name}>"

    def __str__(self):
        return self.name