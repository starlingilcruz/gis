
import uvicorn
from typing import List
from fastapi import FastAPI
from fastapi.responses import \
    JSONResponse, \
    FileResponse, \
    RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from geoalchemy2.shape import to_shape

from repository import Property
from exceptions import \
    PropertyNotFoundException, \
    ImageNotFoundException
from schemas import GeoPoint, PropertyLocation, PropertyZone
from utils import geom_plotter, point_plotter


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/redoc')

@app.get(
    "/display/{id}",
    responses={
        200: {
            "content": {"image/jpeg": {}},
            "description": "JPEG Image",
        },
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    },
)
async def display(id: str):
    prop = Property(id)

    if not prop():
        raise PropertyNotFoundException()

    image = prop.find_image()

    if not image:
        raise ImageNotFoundException()

    image_path = f"static/img/{id}.jpeg"
    image.save(image_path, format="JPEG")

    return FileResponse(path=image_path, media_type='image/jpeg')


@app.get(
    "/display/{id}/overlays",
    responses={
        200: {
            "content": {"image/jpeg": {}},
            "description": "Fetches and displays property image (as JPEG) by ID, with feature overlays drawn on image",
        },
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    },
)
async def display_overlays(
    id: str, geocode_color="blue", parcel_color="orange", \
        building_color="green"
):
    prop = Property(id)

    if not prop():
        raise PropertyNotFoundException()

    image = prop.find_image()

    img_overlayed = geom_plotter(
        image, prop.image_bounds, to_shape(prop.parcel_geo), parcel_color
    )
    img_overlayed = geom_plotter(
        img_overlayed, prop.image_bounds, to_shape(prop.building_geo), \
            building_color
    )
    img_overlayed = point_plotter(
        img_overlayed, prop.image_bounds, to_shape(prop.geocode_geo).coords, \
            geocode_color
    )

    overlay_image_path = f"static/img/{id}-overlay.jpeg"
    img_overlayed.save(overlay_image_path, format="JPEG")

    return FileResponse(path=overlay_image_path, media_type='image/jpeg')


@app.post(
    "/find",
    response_model=List[PropertyLocation],
    responses={
        200: {
            "content": {
                "application/json": {
                    "example": [
                        {
                            "property_id": "f853874999424ad2a5b6f37af6b56610", 
                            "distance_m": 100 
                        }
                    ]
                }
            },
            "description": """
                JSON array with objects with property_id and distance_m fields
            """,
        },
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    }
)
async def find(geo_point: GeoPoint):
    properties = Property.from_geo_point_radius(
        geo_point.location, geo_point.distance_m
    )
    return JSONResponse(properties)


@app.get(
    "/statistics/{id}",
    response_model=PropertyZone,
    responses={
        200: {
            "content": {"application/json": {}},
            "description": """ Returns various statistics for parcels and 
                buildings found X meters around the requested property """,
        },
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    },
)
async def statistics(id: str, zone_size_m: int):
    prop = Property(id)

    if not prop():
        raise PropertyNotFoundException()

    parcel_area_sqm, \
    building_area_sqm, \
    building_distance_m = prop.statistics()
    zone_density = prop.zone_density(zone_size_m)

    return JSONResponse({
        'parcel_area_sqm': parcel_area_sqm,
        'building_area_sqm': building_area_sqm,
        'building_distance_m': building_distance_m,
        'zone_density': zone_density,
    })

# extra
@app.get(
    "/neighbords/{id}",
    responses={
        200: {
            "content": {"application/json": {}},
            "description": """ Return near properties from property reference """,
        },
        404: {"description": "Not found"},
        500: {"description": "Internal server error"}
    },
)
async def neighbords(id: str, distance_m: int):

    prop = Property(id)

    if not prop():
        raise PropertyNotFoundException()

    neighbords = prop.nearby_properties_area(distance_m)

    return JSONResponse({
        'radius': distance_m,
        'coordinates': prop.coordinates,
        'properties': neighbords
    })



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)