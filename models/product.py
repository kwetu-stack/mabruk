from models import db


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    supplier_id = db.Column(
        db.Integer,
        db.ForeignKey("suppliers.id"),
        nullable=False
    )

    brand = db.Column(
        db.String(150),
        nullable=False
    )

    variant = db.Column(
        db.String(100),
        nullable=False
    )

    display_name = db.Column(
        db.String(250),
        nullable=False,
        unique=True
    )

    selling_price = db.Column(
        db.Float,
        default=0
    )

    vat_enabled = db.Column(
        db.Boolean,
        nullable=False,
        default=True
    )

    vat_rate = db.Column(
        db.Float,
        nullable=False,
        default=16
    )

    active = db.Column(
        db.Boolean,
        default=True
    )

    def __repr__(self):
        return f"<Product {self.display_name}>"