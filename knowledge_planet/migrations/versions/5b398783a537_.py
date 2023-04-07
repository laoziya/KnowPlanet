"""empty message

Revision ID: 5b398783a537
Revises: 6267c882a5ef
Create Date: 2023-04-05 15:53:56.946526

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5b398783a537'
down_revision = '6267c882a5ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('lesson_paragraph', 'content_type')
    op.drop_column('lesson_paragraph', 'order')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lesson_paragraph', sa.Column('order', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))
    op.add_column('lesson_paragraph', sa.Column('content_type', mysql.VARCHAR(length=20), nullable=False))
    # ### end Alembic commands ###