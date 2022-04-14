"""add column age

Revision ID: 05da143da2e9
Revises: 3918b7a3aec0
Create Date: 2020-04-29 01:14:57.513381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'v257seq002'
down_revision = 'v257seq001'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'account',
        sa.Column('age', sa.String(3))
    )
    print("------in 2.5.7@head sequence 002")


def downgrade():
    op.drop_column('account', 'age')
