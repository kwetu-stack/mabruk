from flask import Blueprint, jsonify, request

from models.product import Product

api_bp = Blueprint(
    "api",
    __name__,
    url_prefix="/api"
)


@api_bp.route("/products")
def search_products():

    q = request.args.get("q", "").strip()

    if not q:
        return jsonify([])

    products = Product.query.filter(
        Product.display_name.ilike(f"%{q}%")
    ).order_by(
        Product.display_name
    ).limit(10).all()

    return jsonify([
    {
        "id": product.id,
        "name": product.display_name,
        "price": product.selling_price
    }
    for product in products
])