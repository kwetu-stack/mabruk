import os
import unittest

from app import create_app
from models.product import Product


class StartupSeedTestCase(unittest.TestCase):
    def setUp(self):
        self.previous_database_url = os.environ.get("DATABASE_URL")
        os.environ["DATABASE_URL"] = "sqlite:///:memory:"
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()
        if self.previous_database_url is None:
            os.environ.pop("DATABASE_URL", None)
        else:
            os.environ["DATABASE_URL"] = self.previous_database_url

    def test_startup_seeds_products_from_master_workbook(self):
        self.assertGreater(Product.query.count(), 0)

    def test_new_receipt_recovers_from_stale_session_receipt(self):
        with self.app.test_client() as client:
            with client.session_transaction() as session:
                session["receipt_id"] = 999999

            response = client.get("/receipts/new")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Receipt-X", response.data)


if __name__ == "__main__":
    unittest.main()
