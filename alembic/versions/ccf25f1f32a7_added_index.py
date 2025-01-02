"""added index

Revision ID: ccf25f1f32a7
Revises: 759bb2fde9bf
Create Date: 2025-01-02 23:45:00.223360

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ccf25f1f32a7'
down_revision: Union[str, None] = '759bb2fde9bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_laptop_color', 'laptop', ['color'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_laptop_color', table_name='laptop')
    # ### end Alembic commands ###
