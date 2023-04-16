# from sqlalchemy.dialects.sqlite import DOUBLE_PRECISION, UUID
from sqlalchemy import Column, Integer, String, JSON, DateTime, Boolean, Float, Text

from src.database import Base


class UaLocationsSettlement(Base):
    __tablename__ = 'ua_settlements'

    id = Column(Integer(), primary_key=True, nullable=False)
    uuid = Column(Text(length=36), unique=True, nullable=False)
    meta = Column(JSON())
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)
    type = Column(String())
    name = Column(JSON())
    name_lower = Column(String(), nullable=False, index=True)
    post_code = Column(JSON())
    katottg = Column(String())
    koatuu = Column(String())
    lng = Column(Float())
    lat = Column(Float())
    coordinates_added_manually = Column(Boolean(), nullable=False, default=False)
    parent_id = Column(Integer())
    public_name = Column(JSON())

    # https://dba.stackexchange.com/questions/72641/checking-whether-two-tables-have-identical-content-in-postgresql

    def __repr__(self):
        return f"id='{self.id}', name='{self.name['uk']}', {self.lat}, {self.lng}"


class ImportSuccessFlag(Base):
    __tablename__ = 'import_success_flag'

    id = Column(Integer(), primary_key=True, nullable=False)
    finished_at = Column(DateTime(), nullable=False)
    success = Column(Boolean(), nullable=False, default=False)

    def __repr__(self):
        return f"id='{self.id}', success='{self.success}', finished_at={self.finished_at}"
