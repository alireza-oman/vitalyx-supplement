from flask import Blueprint, abort, render_template, request

from app.models import Category, Product

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    selected_category = request.args.get("category", type=str)

    categories = (
        Category.query.filter_by(is_active=True)
        .order_by(Category.name.asc())
        .all()
    )

    product_query = Product.query.filter_by(is_active=True)

    if selected_category:
        product_query = product_query.join(Category).filter(
            Category.slug == selected_category,
            Category.is_active.is_(True),
        )

    products = product_query.order_by(Product.created_at.desc()).all()

    return render_template(
        "home.html",
        products=products,
        categories=categories,
        selected_category=selected_category,
    )


@main_bp.route("/product/<slug>")
def product_detail(slug):
    product = Product.query.filter_by(
        slug=slug,
        is_active=True,
    ).first_or_404()

    return render_template(
        "product_detail.html",
        product=product,
    )


@main_bp.route("/test")
def test():
    abort(403)