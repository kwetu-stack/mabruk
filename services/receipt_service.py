from datetime import datetime

from models.receipt import Receipt


def generate_receipt_number():
    """
    Generate the next receipt number.

    Format:
    AS-YYYY-000001
    """

    year = datetime.now().year

    latest_receipt = (
        Receipt.query
        .filter(
            Receipt.receipt_number.like(f"AS-{year}-%")
        )
        .order_by(Receipt.id.desc())
        .first()
    )

    if latest_receipt is None:
        sequence = 1

    else:
        last_sequence = int(
            latest_receipt.receipt_number.split("-")[-1]
        )

        sequence = last_sequence + 1

    return f"AS-{year}-{sequence:06d}"