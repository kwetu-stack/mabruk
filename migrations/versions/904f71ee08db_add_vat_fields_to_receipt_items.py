"""Add VAT fields to receipt items

Revision ID: 904f71ee08db
Revises: 44fbbdad28f0
Create Date: 2026-07-09 20:57:58.374289

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "904f71ee08db"
down_revision = "44fbbdad28f0"
branch_labels = None
depends_on = None


def upgrade():

    with op.batch_alter_table("receipt_items") as batch_op:

        batch_op.add_column(
            sa.Column(
                "vat_rate",
                sa.Float(),
                nullable=False,
                server_default="0",
            )
        )

        batch_op.add_column(
            sa.Column(
                "vat_amount",
                sa.Float(),
                nullable=False,
                server_default="0",
            )
        )


def downgrade():

    with op.batch_alter_table("receipt_items") as batch_op:

        batch_op.drop_column("vat_amount")
        batch_op.drop_column("vat_rate")