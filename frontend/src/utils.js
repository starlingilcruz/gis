import { Marker, Polyline, InfoWindow } from 'google-maps-react';

import config from './config.json';

export const redirect = (id) => {
  window.open(`${config.API_HOST}/display/${id}/overlays`, '_blank');
};

export const parseCoords = (coords) => {
  const [ lng, lat ] = coords.split(',');
  return {
    lng: parseFloat(lng), 
    lat: parseFloat(lat) 
  }
}

export const renderProperties = (propMap) =>  {
  return propMap.map((p, i) => (
    <Marker
      id={p.id}
      key={i}
      text={`Property ${i}`}
      position={p.center}
      onClick={() => redirect(p.id)}
    />
  ));
}

export const renderPolylines = (targetCoords, propMap) => {
  return propMap.map((p, i) => (
    <Polyline 
      key={i}
      path={[targetCoords, p.center]} 
      options={{ 
        strokeColor: '#ff0000',
        strokeOpacity: 0.5,
        strokeWeight: 2,
      }}
    />
  ))
}