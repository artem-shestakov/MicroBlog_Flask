"""empty message

Revision ID: 79fd77b62c26
Revises: 5faec0552c5b
Create Date: 2020-07-16 02:13:15.703585

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '79fd77b62c26'
down_revision = '5faec0552c5b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'email')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', mysql.VARCHAR(length=80), nullable=True))
    # ### end Alembic commands ###