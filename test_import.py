from app import app
from services.import_service import ImportService

with app.app_context():

    result = ImportService.import_suppliers(
        "ALASKAN/ALASKAN.xlsx"
    )

    print(result)