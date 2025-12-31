"""Add GIN index for metadata_json

Revision ID: b2d0a19d3a89
Revises: b099c1bd0476
Create Date: 2025-12-31 15:16:38.417001

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2d0a19d3a89'
down_revision: Union[str, Sequence[str], None] = 'b099c1bd0476'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    # Включаем расширение pg_trgm для работы с индексами
    op.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm')
    
    # Создаём GIN индекс для текстового представления JSON поля
    # ПРАВИЛЬНЫЙ синтаксис для PostgreSQL:
    op.execute(
        'CREATE INDEX ix_artworks_metadata_json_gin ON artworks '
        'USING gin ((metadata_json::text) gin_trgm_ops)'
    )
    
def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_artworks_metadata_json_gin')
    # Расширение pg_trgm не удаляем, чтобы не сломать другие индексы