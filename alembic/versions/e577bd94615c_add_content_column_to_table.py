"""add content column to table

Revision ID: e577bd94615c
Revises: bd41142a7853
Create Date: 2023-06-10 21:02:15.046574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e577bd94615c'
down_revision = 'bd41142a7853'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
