"""empty message

Revision ID: 6267c882a5ef
Revises: 591f85c18b36
Create Date: 2023-04-03 20:44:35.592064

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6267c882a5ef'
down_revision = '591f85c18b36'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('lesson', 'description')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lesson', sa.Column('description', mysql.TEXT(), nullable=True))
    # ### end Alembic commands ###
