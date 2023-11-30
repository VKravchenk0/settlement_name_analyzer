from sqlalchemy import Column, Integer, String, JSON, DateTime, Boolean, Float, Text
from app.db.database import db


class UaLocationsSettlement(db.Model):
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
    parent_id = Column(Integer())
    public_name = Column(JSON())
    state = Column(String())
    district = Column(String())
    community = Column(String())
    update_file_name = Column(String())


    # https://dba.stackexchange.com/questions/72641/checking-whether-two-tables-have-identical-content-in-postgresql

    def __repr__(self):
        return f"id='{self.id}', name='{self.name['uk']}', {self.lat}, {self.lng}"
