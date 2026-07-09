from models import db


class Supplier(db.Model):
    __tablename__ = "suppliers"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), unique=True, nullable=False)

    contact_person = db.Column(db.String(100))

    phone = db.Column(db.String(30))

    email = db.Column(db.String(120))

    active = db.Column(db.Boolean, default=True)

    products = db.relationship(
        "Product",
        backref="supplier",
        lazy=True
    )

    def __repr__(self):
        return f"<Supplier {self.name}>"