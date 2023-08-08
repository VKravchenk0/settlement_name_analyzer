"""Save locations to db

Revision ID: f99dc27803fb
Revises: 02ae4bf3f067
Create Date: 2023-08-07 23:39:26.637847

"""
from alembic import op
import sqlalchemy as sa
from src.ua_locations_db_importer import save_ua_locations_from_json_to_db


# revision identifiers, used by Alembic.
revision = 'f99dc27803fb'
down_revision = '02ae4bf3f067'
branch_labels = None
depends_on = None


def upgrade():
    save_ua_locations_from_json_to_db()


def downgrade():
    pass
