"""Update locations

Revision ID: 002c1342ce83
Revises: f99dc27803fb
Create Date: 2023-08-08 16:35:10.520535

"""

from app.db.migration.locations_db_importer import execute_updates

# revision identifiers, used by Alembic.
revision = '002c1342ce83'
down_revision = 'f99dc27803fb'
branch_labels = None
depends_on = None


def upgrade():
    execute_updates()


def downgrade():
    pass
