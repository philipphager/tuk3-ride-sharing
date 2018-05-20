import React from 'react';
import PropTypes from 'prop-types';
import DeckGL, { GeoJsonLayer } from 'deck.gl';

const DeckGlLayer = ({ data, viewport }) => {
  const layers = data.map((trajectoryData, index) => {
    return new GeoJsonLayer({
      id: index,
      data: trajectoryData,
      pickable: true,
      stroked: false,
      filled: true,
      extruded: true,
      lineWidthScale: 10,
      lineWidthMinPixels: 2,
      getLineColor: d => d.properties.color,
    });
  });

  return (
    <DeckGL {...viewport} layers={[layers]} />
  );
};

/* eslint-disable */
DeckGlLayer.propTypes = {
  data: PropTypes.any.isRequired,
  viewport: PropTypes.any.isRequired
};
/* eslint-enable */

export default DeckGlLayer;
