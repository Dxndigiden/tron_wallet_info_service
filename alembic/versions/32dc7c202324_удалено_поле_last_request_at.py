"""Удалено поле last_request_at

Revision ID: 32dc7c202324
Revises: 2e5c474488cf
Create Date: 2025-03-31 23:35:32.218720

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32dc7c202324'
down_revision: Union[str, None] = '2e5c474488cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('walletinfo', 'last_request_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('walletinfo', sa.Column('last_request_at', sa.DATETIME(), nullable=False))
    # ### end Alembic commands ###
