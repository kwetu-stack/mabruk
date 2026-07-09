import os
import sys
import logging
import traceback

from flask import Flask
from werkzeug.exceptions import HTTPException

from config import Config
from models import db, login_manager
from flask_migrate import Migrate

from routes.auth import auth_bp
from routes.products import products_bp
from routes.receipts import receipts_bp
from routes.api import api_bp
from routes.dashboard import dashboard_bp

from services.import_service import ImportService
from services.user_service import create_user


def seed_initial_products(app):
    with app.app_context():
        from models.product import Product

        if Product.query.first():
            return

        product_master_path = os.path.join(
            app.root_path,
            "PRODUCT_MASTER",
            "RECEIPT-X_PRODUCT_MASTER.xlsx",
        )

        if not os.path.exists(product_master_path):
            app.logger.warning(
                "Product master workbook not found at %s",
                product_master_path,
            )
            return

        try:
            result = ImportService.import_products(product_master_path)

            app.logger.info(
                "Seeded %s products from %s",
                result.get("created", 0),
                product_master_path,
            )

        except Exception as exc:
            app.logger.exception(
                "Initial product seeding failed: %s",
                exc,
            )


def initialize_database(app):
    with app.app_context():

        from models.user import User
        from models.supplier import Supplier
        from models.product import Product
        from models.receipt import Receipt
        from models.receipt_item import ReceiptItem

        db.create_all()

        create_user(
            full_name="System Administrator",
            username="admin",
            password=os.environ.get("ADMIN_PASSWORD", "admin123"),
            role="ADMIN",
        )

        create_user(
            full_name="BALOZI",
            username="balozi",
            password="balozi123",
            role="INVOICER",
        )

        create_user(
            full_name="ERIC",
            username="eric",
            password="eric123",
            role="INVOICER",
        )

        create_user(
            full_name="PRUDENCE",
            username="prudence",
            password="prudence123",
            role="INVOICER",
        )

        create_user(
            full_name="TUVA",
            username="tuva",
            password="tuva123",
            role="INVOICER",
        )

        seed_initial_products(app)


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)
    login_manager.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(receipts_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(dashboard_bp)

    @app.route("/health")
    def health():
        return {"status": "ok"}

    @app.errorhandler(Exception)
    def log_exception(error):
        if isinstance(error, HTTPException):
            return error

        app.logger.error("Unhandled exception: %s", error)
        app.logger.error(traceback.format_exc())

        return "Internal Server Error", 500

    # Skip initialization when running Flask-Migrate commands
    if "db" not in sys.argv:
        initialize_database(app)

    return app


logging.basicConfig(level=logging.INFO)

app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True,
    )