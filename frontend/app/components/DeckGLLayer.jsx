import React from 'react';
import PropTypes from 'prop-types';
import DeckGL, { GeoJsonLayer } from 'deck.gl';

const DeckGlLayer = ({ data, viewport }) => {
  const layer = new GeoJsonLayer({
    id: 'geojson-layer',
    data,
    pickable: true,
    stroked: false,
    filled: true,
    extruded: true,
    lineWidthScale: 20,
    lineWidthMinPixels: 2,
    /*
    getFillColor: data => [160, 160, 180, 200],
    getLineColor: d => colorToRGBArray(d.properties.color),
    getRadius: d => 100,
    getLineWidth: d => 1,
    getElevation: d => 30,
    onHover: ({object}) => setTooltip(object.properties.name || object.properties.station) */
  });
  return (
    <DeckGL {...viewport} layers={[layer]} />
  );
};

/* eslint-disable */
DeckGlLayer.propTypes = {
  // eslint-disable-next-line
  data: PropTypes.any.isRequired,
  viewport: PropTypes.any.isRequired
};
/* eslint-enable */

export default DeckGlLayer;
