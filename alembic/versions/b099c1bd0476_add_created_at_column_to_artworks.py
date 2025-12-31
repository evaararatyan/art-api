"""Add created_at column to artworks

Revision ID: b099c1bd0476
Revises: 
Create Date: 2025-12-31 15:16:20.177333

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b099c1bd0476'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Добавляем колонку created_at
    op.add_column('artworks', sa.Column('created_at', sa.DateTime(), nullable=True))
    
    # Заполняем существующие записи текущим временем
    op.execute("UPDATE artworks SET created_at = NOW()")
    
    # Делаем колонку обязательной
    op.alter_column('artworks', 'created_at', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Удаляем колонку created_at
    op.drop_column('artworks', 'created_at')