"""add column email

Revision ID: v256seq002
Revises: v256seq001
Create Date: 2020-04-29 01:14:57.513381

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'v256seq002'
down_revision = 'v256seq001'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'account',
        sa.Column('email', sa.String(20))
    )
    print("------in 2.5.6@head sequence 002")


def downgrade():
    op.drop_column('account', 'email')
