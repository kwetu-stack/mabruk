from app import app
from services.import_service import ImportService

with app.app_context():

    result = ImportService.import_products(
        "PRODUCT_MASTER/RECEIPT-X_PRODUCT_MASTER.xlsx"
    )

    print(result)