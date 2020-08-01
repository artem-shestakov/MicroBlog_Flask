"""empty message

Revision ID: d1b42e145949
Revises: bd74c031d5b5
Create Date: 2020-08-02 00:29:47.472308

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd1b42e145949'
down_revision = 'bd74c031d5b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('email', table_name='users')
    op.drop_column('users', 'email')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', mysql.VARCHAR(length=255), nullable=False))
    op.create_index('email', 'users', ['email'], unique=True)
    # ### end Alembic commands ###
