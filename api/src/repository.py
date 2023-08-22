import json
import requests
from typing import List
from database import Session
from models import Properties
from schemas import PropertyLocation

from sqlalchemy import func
from geoalchemy2.shape import to_shape
from geoalchemy2.functions import ST_Buffer
from geojson import Point

from io import BytesIO
from PIL import Image



class Property:

    db = Session()
    
    def __init__(self, id: str, **kwargs) -> None:
        self.prop = Property.find_by_id(id)

    def __call__(self):
        return self.prop
        
    def __repr__(self) -> str:
        return f'Property Geo Point: { to_shape(self.prop.geocode_geo) }'

    @classmethod
    def find_by_id(cls, id: str):
        return cls.db.query(Properties).filter(Properties.id == id).first()

    @property
    def coordinates(self):
        return f"{to_shape(self.prop.geocode_geo).x}, {to_shape(self.prop.geocode_geo).y}"

    @property
    def parcel_geo(self):
        return self.prop.parcel_geo

    @property
    def building_geo(self):
        return self.prop.building_geo

    @property
    def geocode_geo(self):
        return self.prop.geocode_geo

    @property
    def image_bounds(self):
        return self.prop.image_bounds

    @property
    def image_url(self):
        return self.prop.image_url

    def find_image(self):
        # TODO look for cached image
        if not self.prop:
            return None

        with requests.get(self.image_url, stream=True) as r:
            buffer = BytesIO(r.content)
            return Image.open(buffer)

    @classmethod
    def from_geo_point_radius(
        cls, geo_point: Point, distance_m: float
    ) -> List[PropertyLocation]:
        # calculates the distance between geocode and geo json point
        properties = cls.db.query(
            Properties.id.label("property_id"), 
            func.ST_Distance(
                Properties.geocode_geo, 
                func.ST_GeomFromGeoJSON(json.dumps(geo_point))
            ).label("distance_m")
        ).filter(
            func.ST_DWithin(
                Properties.geocode_geo, 
                func.ST_GeomFromGeoJSON(json.dumps(geo_point)),
                distance_m
            )
        ).all()

        return [{
            "property_id": p.property_id,
            "distance_m": p.distance_m 
        } for p in properties]

    def zone_density(self, zone_size_m):
        row = self.db.query(
            func.SUM(
                (func.ST_Area(
                    func.ST_Intersection(
                        Properties.building_geo,
                        ST_Buffer(Properties.geocode_geo, zone_size_m)
                    )
                ) / func.ST_Area(func.ST_Buffer(Properties.geocode_geo, zone_size_m))) * 100
            ).label('density_p')
        ).filter(
            Properties.id == self.prop.id
        ).first()

        return row.density_p
        
    def statistics(self):
        return self.db.query(
            func.ST_Area(Properties.parcel_geo).label("parcel_area_sqm"),
            func.ST_Area(Properties.building_geo).label("building_area_sqm"),
            func.ST_Distance(
                Properties.geocode_geo, 
                func.ST_Centroid(Properties.building_geo),
            ).label("building_distance_m"),
        ).filter(Properties.id == self.prop.id).first()

    # extra
    def nearby_properties_area(self, distance_m):
        """ Find near properties info within given distance.

            Area includes all polygons regardless of whether some 
            are outside the radius.
        """

        properties = self.db.query(
            Properties.id,
            Properties.geocode_geo,
            func.ST_Area(Properties.parcel_geo).label("parcel_area_sqm"),
            func.ST_Area(Properties.building_geo).label("building_area_sqm"),
            func.ST_Distance(
                Properties.geocode_geo, 
                func.ST_Centroid(self.geocode_geo),
            ).label("centroid_distance_m"),
        ).filter(
            func.ST_DWithin(
                Properties.geocode_geo, 
                self.geocode_geo, 
                distance_m
            ),
            Properties.id != self.prop.id
        ).all()

        return [{
            "id": p.id,
            "coordinates": f"""
                { to_shape(p.geocode_geo).x }, { to_shape(p.geocode_geo).y }
                """,
            "parcel_area_sqm": p.parcel_area_sqm,
            "building_area_sqm": p.building_area_sqm,
            "distance_m": p.centroid_distance_m 
        } for p in properties]

        
        