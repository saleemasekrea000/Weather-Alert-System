"""weather model

Revision ID: c7d58bb99064
Revises:
Create Date: 2025-02-14 01:07:18.503258

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c7d58bb99064"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "weather",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("city", sa.String(), nullable=False),
        sa.Column("temperature", sa.Float(), nullable=False),
        sa.Column("humidity", sa.Integer(), nullable=False),
        sa.Column("wind_speed", sa.Float(), nullable=False),
        sa.Column("pressure", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_weather_city"), "weather", ["city"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_weather_city"), table_name="weather")
    op.drop_table("weather")
    # ### end Alembic commands ###
