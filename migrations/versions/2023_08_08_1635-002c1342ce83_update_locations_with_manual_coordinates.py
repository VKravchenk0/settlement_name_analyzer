"""Update locations with manual coordinates

Revision ID: 002c1342ce83
Revises: f99dc27803fb
Create Date: 2023-08-08 16:35:10.520535

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from src.ua_locations_db_importer import update_settlements_with_manual_coordinates

revision = '002c1342ce83'
down_revision = 'f99dc27803fb'
branch_labels = None
depends_on = None


def upgrade():
    update_settlements_with_manual_coordinates()


def downgrade():
    pass
