"""add avtive filed to the alert table

Revision ID: 9546e34ab9c5
Revises: 167403e1b8c9
Create Date: 2025-02-15 03:05:45.737311

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9546e34ab9c5"
down_revision: Union[str, None] = "167403e1b8c9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("alerts", sa.Column("is_active", sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("alerts", "is_active")
    # ### end Alembic commands ###
