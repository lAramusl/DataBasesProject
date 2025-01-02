"""added color

Revision ID: 759bb2fde9bf
Revises: 87077da146c4
Create Date: 2025-01-02 22:14:35.599605

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '759bb2fde9bf'
down_revision: Union[str, None] = '87077da146c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('laptop', sa.Column('color', sa.VARCHAR(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('laptop', 'color')
    # ### end Alembic commands ###
