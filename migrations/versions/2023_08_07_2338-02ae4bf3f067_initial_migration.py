"""Initial migration

Revision ID: 02ae4bf3f067
Revises: 
Create Date: 2023-08-07 23:38:51.817320

"""
from app.db.database import db


# revision identifiers, used by Alembic.
revision = '02ae4bf3f067'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """
    Using create_all instead of column-by-column creation, since in our case it's acceptable and easier to
    recreate the DB from scratch each time
    """
    db.create_all()


def downgrade():
    pass
