"""empty message

Revision ID: d97b6fe5b90f
Revises: e7e9368ba4a3
Create Date: 2023-03-25 14:18:43.922850

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd97b6fe5b90f'
down_revision = 'e7e9368ba4a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('gender', sa.String(length=10), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'gender')
    # ### end Alembic commands ###
