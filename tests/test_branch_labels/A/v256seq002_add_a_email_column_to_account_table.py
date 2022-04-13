"""Add a email column to account table

Revision ID: 05da143da2e9
Revises: 3918b7a3aec0
Create Date: 2020-04-29 01:14:57.513381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'v256seq002'
down_revision = 'v256seq001'
branch_labels = '2.5.6_B'
depends_on = None


def upgrade():
    op.add_column(
        'account',
        sa.Column('email', sa.String(20))
    )


def downgrade():
    op.drop_column('account', 'email')
