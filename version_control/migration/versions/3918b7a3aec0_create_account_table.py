"""create account table

Revision ID: 3918b7a3aec0
Revises:
Create Date: 2020-04-29 01:05:52.377396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3918b7a3aec0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'account',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(64), nullable=False),
        sa.Column('description', sa.Unicode(200)),
    )
    print("------in base@head")


def downgrade():
    op.drop_table('account')
