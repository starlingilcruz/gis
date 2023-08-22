# Geographic Information System


API fundamental frameworks: 

* [FastAPI](https://fastapi.tiangolo.com/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [GeoAlchemy](https://geoalchemy-2.readthedocs.io/en/latest/)


Client application:

* React: as an addition to the test, I created a very basic application to consume the "neighbords" endpoint. This displays information about the properties found in an determinated radius, taking a property as a reference point. Each property found is displayed with a marker, clicking on the marker open up an `Info Window` with key property information.


- Limitations:
There is not form in the [client app](http://localhost:3000/?id=622088210a6f43fca2a1824e8610df03&distance=60000)
 to pass the *property_id* and *distance*. So, those can only be assigned through query params.

### Feature List

See the complete openAPI specs: [http://localhost:8000/redoc](http://localhost:8000/redoc)

* **Display:** API endpoint to display an image by property ID. Given a *propertyId* as input, 
  find the image URL from the database, download it from Google Cloud Storage and return a JPEG image. 
  
* **Find:** API endpoint to search properties within a geographical area. 
  Take a [GeoJSON](https://geojson.org/) object *geoJson* and a search radius *distance* 
  (in meters) as inputs. Return all property IDs that are within *distance* meters of *geoJson*. 
  
* **Display Plus:** An alternative version of the first API endpoint (**Display**) to also 
  overlay the geocode (as a marker - such as a small circle or triangle), parcel, 
  and/or building (`geocode_geo`, `parcel_geo`, and `building_geo` fields in the database, respectively)
  on the image. Optionally, add parameters for the color of each overlay, or use a default for each. 
  
* **Statistics:** API endpoint to calculate geographic data about all properties within a given 
  distance from a reference property. Take *propertyId* and *distance* (in meters) as inputs. 
  The API should return the following:
  * parcel area (meters squared)
  * building area (meters squared)
  * building distance to center (meters). Distance to center is the distance from the 
    building to the `geocode_geo` field in the property table
  * zone density (percentage). Create a "zone" geography, which is a buffer of *distance* 
    meters around the `geocode_geo` point. Then, calculate the percentage of that zone geography 
    which has buildings in it. 

* **Neighbords (Additional):** API endpoint to retrive list of properties within a given 
  distance from a reference property. Take *propertyId* and *distance* (in meters) as inputs.
  The propurse of this endpoint is for be consumed by the [client application](http://localhost:3000/?id=622088210a6f43fca2a1824e8610df03&distance=60000)


### How to Run

```
docker-compose up
```

### How to run the tests
You can run the tests by accessing the container and from there executing a bash script 'test.sh' inside the scripts directory.

```
bash scripts/test.sh
```

To generate coverage reports:

```
pytest --cov=. --cov-report=xml
```
### Links
* API: [http://localhost:8000](http://localhost:8000)
* React App: [http://localhost:3000](http://localhost:3000/?id=622088210a6f43fca2a1824e8610df03&distance=60000)
