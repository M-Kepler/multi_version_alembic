"""add column address

Revision ID: db1912e824e8
Revises: 05da143da2e9
Create Date: 2020-04-29 01:24:28.916821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'v256seq001'
down_revision = '3918b7a3aec0'
branch_labels = '2.5.6_B'
depends_on = None


def upgrade():
    op.add_column(
        'account',
        sa.Column('address', sa.String(20))
    )


def downgrade():
    op.drop_column('account', 'address')
    pass
