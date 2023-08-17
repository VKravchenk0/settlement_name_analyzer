"""Set state, district, community values

Revision ID: 7e78a0acfa34
Revises: 002c1342ce83
Create Date: 2023-08-16 23:40:15.518077

"""

from app.db.crud import execute_native_sql_from_file

# revision identifiers, used by Alembic.
revision = '7e78a0acfa34'
down_revision = '002c1342ce83'
branch_labels = None
depends_on = None


def upgrade():
    execute_native_sql_from_file('./migrations/scripts/2023_08_16_2340-7e78a0acfa34_set_state_district_community_values.sql')


def downgrade():
    pass
