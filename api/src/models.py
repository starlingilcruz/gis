from database import Base
from sqlalchemy import Column, String, Float
from geoalchemy2 import Geography


class Properties(Base):
    
    __tablename__ = 'properties'

    id = Column(String, primary_key=True)
    geocode_geo = Column(Geography(geometry_type='POINT', srid=4326))
    parcel_geo = Column(Geography(geometry_type='POLYGON', srid=4326))
    building_geo = Column(Geography(geometry_type='POLYGON', srid=4326))
    image_bounds = Column(Float)
    image_url = Column(String)
