from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify,
)
from flask_login import login_required, current_user

from models import db
from models.product import Product
from models.receipt import Receipt
from models.receipt_item import ReceiptItem

from services.receipt_service import generate_receipt_number


receipts_bp = Blueprint(
    "receipts",
    __name__,
    url_prefix="/receipts",
)

DEFAULT_RECEIPT_CUSTOMER_NAME = "MABROUK SHOP ALASKAN"


# ----------------------------
# MAIN SCREEN
# ----------------------------
@receipts_bp.route("/new", methods=["GET"])
@login_required
def new_receipt():

    receipt = None
    receipt_id = session.get("receipt_id")

    if receipt_id is not None:
        receipt = db.session.get(Receipt, receipt_id)

    if receipt is None:

        receipt = Receipt(
            receipt_number=generate_receipt_number(),
            customer_name="",
            created_by=current_user.id,
            total_amount=0,
            status="OPEN",
        )

        db.session.add(receipt)
        db.session.commit()

        session["receipt_id"] = receipt.id

    products = Product.query.order_by(
        Product.display_name
    ).all()

    items = ReceiptItem.query.filter_by(
        receipt_id=receipt.id
    ).all()

    total = sum(item.total for item in items)

    return render_template(
        "receipts/new.html",
        receipt=receipt,
        products=products,
        items=items,
        total=total,
    )


# ----------------------------
# ADD ITEM
# ----------------------------
@receipts_bp.route("/add-item", methods=["POST"])
@login_required
def add_item():

    if "receipt_id" not in session:
        return redirect(url_for("receipts.new_receipt"))

    receipt_id = session["receipt_id"]

    product_id = int(request.form["product_id"])
    quantity = float(request.form["quantity"])
    unit_price = float(request.form["unit_price"])

    product = db.session.get(Product, product_id)

    vat_rate = 0
    vat_amount = 0

    if product and product.vat_enabled:

        vat_rate = product.vat_rate

        line_total = quantity * unit_price

        vat_amount = line_total - (
            line_total / (1 + (vat_rate / 100))
        )

    total = quantity * unit_price

    item = ReceiptItem(
        receipt_id=receipt_id,
        product_id=product_id,
        quantity=quantity,
        unit_price=unit_price,
        vat_rate=vat_rate,
        vat_amount=vat_amount,
        total=total,
    )

    db.session.add(item)
    db.session.commit()

    receipt = db.session.get(Receipt, receipt_id)

    receipt.total_amount = sum(
        i.total for i in receipt.items
    )

    db.session.commit()

    return redirect(
        url_for("receipts.new_receipt")
    )


# ----------------------------
# AJAX ADD ITEM
# ----------------------------
@receipts_bp.route("/api/add-item", methods=["POST"])
@login_required
def api_add_item():

    if "receipt_id" not in session:
        return jsonify(
            {"error": "No active receipt"}
        ), 400

    receipt_id = session["receipt_id"]

    data = request.get_json()

    customer_name = data.get(
        "customer_name",
        "Walk-in Customer",
    )

    product_id = int(data["product_id"])
    quantity = float(data["quantity"])
    unit_price = float(data["unit_price"])

    product = db.session.get(Product, product_id)

    vat_rate = 0
    vat_amount = 0

    if product and product.vat_enabled:

        vat_rate = product.vat_rate

        line_total = quantity * unit_price

        vat_amount = line_total - (
            line_total / (1 + (vat_rate / 100))
        )

    total = quantity * unit_price

    item = ReceiptItem(
        receipt_id=receipt_id,
        product_id=product_id,
        quantity=quantity,
        unit_price=unit_price,
        vat_rate=vat_rate,
        vat_amount=vat_amount,
        total=total,
    )

    db.session.add(item)
    db.session.commit()

    receipt = db.session.get(
        Receipt,
        receipt_id,
    )

    receipt.customer_name = customer_name

    receipt.total_amount = sum(
        i.total for i in receipt.items
    )

    db.session.commit()

    return jsonify(
        {
            "success": True,
            "item": {
                "id": item.id,
                "product": item.product.display_name,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "vat_rate": item.vat_rate,
                "vat_amount": item.vat_amount,
                "total": item.total,
            },
            "grand_total": receipt.total_amount,
        }
    )


# ----------------------------
# SAVE RECEIPT
# ----------------------------
@receipts_bp.route("/save", methods=["POST"])
@login_required
def save_receipt():

    if "receipt_id" not in session:
        return redirect(
            url_for("receipts.new_receipt")
        )

    receipt = db.session.get(
        Receipt,
        session["receipt_id"],
    )

    receipt.customer_name = request.form.get(
        "customer_name",
        "Walk-in Customer",
    )

    receipt.total_amount = sum(
        item.total for item in receipt.items
    )

    receipt.status = "SAVED"

    db.session.commit()

    session.pop("receipt_id", None)

    return redirect(
        url_for(
            "receipts.view_receipt",
            receipt_id=receipt.id,
        )
    )
# ----------------------------
# PRINT RECEIPT
# ----------------------------
@receipts_bp.route("/print/<int:receipt_id>")
@login_required
def print_receipt(receipt_id):

    receipt = Receipt.query.get_or_404(
        receipt_id
    )

    items = ReceiptItem.query.filter_by(
        receipt_id=receipt.id
    ).all()

    gross_sales = sum(
        item.total for item in items
    )

    total_vat = sum(
        item.vat_amount for item in items
    )

    net_sales = gross_sales - total_vat

    return render_template(
        "receipts/print.html",
        receipt=receipt,
        items=items,
        gross_sales=gross_sales,
        net_sales=net_sales,
        total_vat=total_vat,
    )

# ----------------------------
# VIEW RECEIPT
# ----------------------------
@receipts_bp.route("/view/<int:receipt_id>")
@login_required
def view_receipt(receipt_id):

    receipt = Receipt.query.get_or_404(
        receipt_id
    )

    items = ReceiptItem.query.filter_by(
        receipt_id=receipt.id
    ).all()

    gross_sales = sum(
        item.total for item in items
    )

    total_vat = sum(
        item.vat_amount for item in items
    )

    net_sales = gross_sales - total_vat

    return render_template(
        "receipts/view.html",
        receipt=receipt,
        items=items,
        gross_sales=gross_sales,
        net_sales=net_sales,
        total_vat=total_vat,
    )


# ----------------------------
# RECEIPT HISTORY
# ----------------------------
@receipts_bp.route("/")
@login_required
def history():

    receipts = (
    Receipt.query
    .filter_by(status="SAVED")
    .order_by(Receipt.id.desc())
    .all()
)

    return render_template(
        "receipts/history.html",
        receipts=receipts,
    )