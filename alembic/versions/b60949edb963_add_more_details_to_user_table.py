"""add more details to user table

Revision ID: b60949edb963
Revises: 6ce206f969c3
Create Date: 2023-06-10 23:18:00.067489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b60949edb963'
down_revision = '6ce206f969c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('firstname', sa.String(), nullable=False))
    op.add_column('users', sa.Column('lastname', sa.String(), nullable=False))
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    pass
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    op.drop_column('users', 'lastname')
    op.drop_column('users', 'firstname')
    pass
    # ### end Alembic commands ###