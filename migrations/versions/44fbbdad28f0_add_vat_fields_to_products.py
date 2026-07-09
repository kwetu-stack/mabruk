"""Add VAT fields to products

Revision ID: 44fbbdad28f0
Revises: dd6079e6c084
Create Date: 2026-07-09 17:52:32.956618

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "44fbbdad28f0"
down_revision = "dd6079e6c084"
branch_labels = None
depends_on = None


def upgrade():

    with op.batch_alter_table("products") as batch_op:

        batch_op.add_column(
            sa.Column(
                "vat_enabled",
                sa.Boolean(),
                nullable=False,
                server_default=sa.true(),
            )
        )

        batch_op.add_column(
            sa.Column(
                "vat_rate",
                sa.Float(),
                nullable=False,
                server_default="16",
            )
        )


def downgrade():

    with op.batch_alter_table("products") as batch_op:

        batch_op.drop_column("vat_rate")
        batch_op.drop_column("vat_enabled")