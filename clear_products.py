from app import app
from models import db
from models.product import Product

with app.app_context():

    deleted = Product.query.delete()

    db.session.commit()

    print(f"{deleted} products deleted.")