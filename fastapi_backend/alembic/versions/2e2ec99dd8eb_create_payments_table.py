"""create payments table

Revision ID: 2e2ec99dd8eb
Revises: d3c1f7abb2fd
Create Date: 2026-10-05 17:39:57.751230

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2e2ec99dd8eb"
down_revision: Union[str, Sequence[str], None] = "d3c1f7abb2fd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "payments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("payment_method", sa.String(length=50), nullable=False),
        sa.Column("transaction_id", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.ForeignKeyConstraint(
            ["order_id"],
            ["orders.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_payments_id"),
        "payments",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_payments_id"),
        table_name="payments",
    )
    op.drop_table("payments")