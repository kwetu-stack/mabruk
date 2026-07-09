from models import db


class ReceiptItem(db.Model):
    __tablename__ = "receipt_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    receipt_id = db.Column(
        db.Integer,
        db.ForeignKey("receipts.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    quantity = db.Column(
        db.Float,
        nullable=False
    )

    unit_price = db.Column(
        db.Float,
        nullable=False
    )

    vat_rate = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    vat_amount = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    total = db.Column(
        db.Float,
        nullable=False
    )

    product = db.relationship(
        "Product",
        backref="receipt_items"
    )

    def __repr__(self):
        return (
            f"<ReceiptItem "
            f"Receipt={self.receipt_id} "
            f"Product={self.product_id}>"
        )