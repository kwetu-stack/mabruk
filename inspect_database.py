from app import app
from models.supplier import Supplier
from models.product import Product
from models.receipt import Receipt
from models.receipt_item import ReceiptItem


with app.app_context():

    print("\n" + "=" * 60)
    print("ALASKAN SALES™ DATABASE INSPECTOR")
    print("=" * 60)

    print(f"\nSuppliers     : {Supplier.query.count()}")
    print(f"Products      : {Product.query.count()}")
    print(f"Receipts      : {Receipt.query.count()}")
    print(f"Receipt Items : {ReceiptItem.query.count()}")

    print("\n" + "=" * 60)
    print("SUPPLIERS")
    print("=" * 60)

    suppliers = Supplier.query.order_by(Supplier.name).all()

    for supplier in suppliers:

        count = Product.query.filter_by(
            supplier_id=supplier.id
        ).count()

        print(f"{supplier.id:>3} | {supplier.name:<30} | {count:>3} products")

    print("\n" + "=" * 60)
    print("FIRST 30 PRODUCTS")
    print("=" * 60)

    products = Product.query.order_by(Product.display_name).limit(30).all()

    for product in products:

        supplier = Supplier.query.get(product.supplier_id)

        print(
            f"{product.id:>3} | "
            f"{supplier.name:<25} | "
            f"{product.display_name}"
        )

    print("\n" + "=" * 60)