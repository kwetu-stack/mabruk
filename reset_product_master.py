from app import app
from models import db
from models.receipt_item import ReceiptItem
from models.receipt import Receipt
from models.product import Product
from models.supplier import Supplier
from services.import_service import ImportService


MASTER_FILE = "RECEIPT-X_PRODUCT_MASTER.xlsx"


with app.app_context():

    print("\n========== RESET PRODUCT MASTER ==========\n")

    receipt_item_count = ReceiptItem.query.delete()
    print(f"Receipt Items Deleted : {receipt_item_count}")

    receipt_count = Receipt.query.delete()
    print(f"Receipts Deleted      : {receipt_count}")

    product_count = Product.query.delete()
    print(f"Products Deleted      : {product_count}")

    supplier_count = Supplier.query.delete()
    print(f"Suppliers Deleted     : {supplier_count}")

    db.session.commit()

    print("\nImporting Suppliers...\n")

    supplier_result = ImportService.import_suppliers(MASTER_FILE)

    print(supplier_result)

    print("\nImporting Products...\n")

    product_result = ImportService.import_products(MASTER_FILE)

    print(product_result)

    print("\n========== COMPLETE ==========\n")