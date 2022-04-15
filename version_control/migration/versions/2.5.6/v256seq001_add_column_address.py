"""add column address

Revision ID: v256seq001
Revises:
Create Date: 2020-04-29 01:24:28.916821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'v256seq001'
down_revision = None
branch_labels = ('2.5.6',)
depends_on = None


def upgrade():
    op.add_column(
        'account',
        sa.Column('address', sa.String(20))
    )
    print("------in 2.5.6@head sequence 001")


def downgrade():
    op.drop_column('account', 'address')
