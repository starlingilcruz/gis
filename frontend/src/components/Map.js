import React from 'react';
import {
  GoogleApiWrapper, 
  Map, 
  Marker, 
  Circle,
  InfoWindow
} from 'google-maps-react';
import config from '../config.json';
import {
  parseCoords,
  renderProperties,
  renderPolylines,
  redirect
} from '../utils';


export class MapContainer extends React.Component {
  state = { activeMarker: {} };

  onMarkerClick = (props, marker) => 
    this.setState({
      activeMarker: marker,
      selectedPlace: props,
      showingInfoWindow: true
    });

  render() {
    const {
      radius,
      coordinates,
      properties
    } = this.props.data;

    const targetPropCoords = parseCoords(coordinates);
    const propMap = properties.map((prop) => ({
      id: prop.id,
      center: parseCoords(prop.coordinates) 
    }));
    
    
    return (
      <Map
        google={this.props.google} 
        zoom={this.props.defaultZoom}
        initialCenter={targetPropCoords}
      >
        <Circle
          radius={radius}
          center={targetPropCoords}
          strokeColor='transparent'
          strokeOpacity={0}
          strokeWeight={5}
          fillColor='#FF0000'
          fillOpacity={0.2}
        />

        <Marker
          key={0}
          position={targetPropCoords}
          onClick={this.onMarkerClick}
        >
        </Marker>

        <InfoWindow
          key={`infowindow`}
          marker={this.state.activeMarker}
          visible={true}>
          <div>
            <ul>
              <li>
                <pre>Coord: { coordinates }</pre>
              </li>
              <li>
                <pre>Radius: { radius } meters</pre>
              </li>
            </ul>
          </div>
        </InfoWindow>
        
        { renderProperties(propMap) }
        { renderPolylines(targetPropCoords, propMap) }
      </Map>
    );
  }
}
 
export default GoogleApiWrapper({ apiKey: config.GOOGLE_API_KEY })(MapContainer)