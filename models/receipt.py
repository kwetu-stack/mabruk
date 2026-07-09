from models import db
from config import now_in_nairobi


class Receipt(db.Model):
    __tablename__ = "receipts"

    id = db.Column(db.Integer, primary_key=True)

    receipt_number = db.Column(db.String(30), unique=True, nullable=False)

    receipt_date = db.Column(db.DateTime, default=now_in_nairobi)

    customer_name = db.Column(db.String(150), nullable=False)

    total_amount = db.Column(db.Float, default=0)

    status = db.Column(db.String(20), default="OPEN")

    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship(
    "User",
    backref="receipts"
)

    items = db.relationship(
        "ReceiptItem", backref="receipt", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Receipt {self.receipt_number}>"
