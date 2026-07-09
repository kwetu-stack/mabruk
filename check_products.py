from app import app
from models.product import Product

with app.app_context():

    print("\n========== PRODUCTS ==========\n")

    for product in Product.query.order_by(Product.display_name):

        print(
            f"{product.display_name:<30} "
            f"Price: {product.selling_price}"
        )