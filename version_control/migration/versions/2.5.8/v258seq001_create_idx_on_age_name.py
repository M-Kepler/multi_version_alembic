"""create index on age and name

Revision ID: v258seq001
Revises:
Create Date: 2020-04-29 01:24:28.916821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'v258seq001'
down_revision = None
branch_labels = ('2.5.8',)
depends_on = None


def upgrade():
    op.create_index(
        'idx_name_and_age',
        'account',
        ['name', 'age']

    )
    print("------in 2.5.8@head sequence 001")


def downgrade():
    op.drop_index('account', 'idx_name_and_age')
