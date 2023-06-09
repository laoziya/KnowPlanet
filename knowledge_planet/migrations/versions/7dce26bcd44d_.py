"""empty message

Revision ID: 7dce26bcd44d
Revises: 8df8b46d3006
Create Date: 2023-03-27 20:09:46.996572

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7dce26bcd44d'
down_revision = '8df8b46d3006'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tag', sa.Column('course_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'tag', 'course', ['course_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tag', type_='foreignkey')
    op.drop_column('tag', 'course_id')
    # ### end Alembic commands ###
