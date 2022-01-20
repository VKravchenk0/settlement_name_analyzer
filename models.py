from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION, UUID
from sqlalchemy import Column, Integer, String, JSON, DateTime

from database import Base


class UaLocationsSettlement(Base):
    __tablename__ = 'ua_settlements'

    id = Column(Integer(), primary_key=True, nullable=False)
    uuid = Column(UUID(), unique=True, nullable=False)
    meta = Column(JSON())
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)
    type = Column(String())
    name = Column(JSON())
    post_code = Column(JSON())
    katottg = Column(String())
    koatuu = Column(String())
    lng = Column(DOUBLE_PRECISION())
    lat = Column(DOUBLE_PRECISION())
    parent_id = Column(Integer())
    public_name = Column(JSON())

    # https://dba.stackexchange.com/questions/72641/checking-whether-two-tables-have-identical-content-in-postgresql

    def __repr__(self):
        return f"id='{self.id}', name='{self.name['uk']}', {self.lat}, {self.lng}"
