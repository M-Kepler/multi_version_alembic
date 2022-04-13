"""add column address

Revision ID: db1912e824e8
Revises: 05da143da2e9
Create Date: 2020-04-29 01:24:28.916821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'v257seq001'
down_revision = None
branch_labels = ('2.5.7',)
depends_on = None


def upgrade():
    op.add_column(
        'account',
        sa.Column('sex', sa.String(2))
    )
    print("------in 2.5.7@head sequence 001")


def downgrade():
    op.drop_column('account', 'sex')
    pass
