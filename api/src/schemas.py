from typing import List
from pydantic import BaseModel, validator
from geojson import Point


class GeoPoint(BaseModel):
    location: Point
    distance_m: float

    @validator('distance_m')
    def min_value(cls, v):
        if v < 0:
            raise ValueError('Distance is smaller than 0')
        return v

    @validator('distance_m')
    def max_value(cls, v):
        if v > 500000:
            raise ValueError('Distance is greather than 500000')
        return v


class PropertyLocation(BaseModel):
    property_id: str
    distance_m: float


class PropertyZone(BaseModel):
    parcel_area_sqm: float
    building_area_sqm: float
    building_distance_m: float
    zone_density: float

class PropertyNeighbor(BaseModel):
    parcel_area_sqm: float
    building_area_sqm: float
    building_distance_m: float
    zone_density: float

class Neighbord(BaseModel):
    radius: float
    coordinates: str
    properties: List[PropertyNeighbor]