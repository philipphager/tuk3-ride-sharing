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
      // onHover: ({ object }) => setTooltip(object.properties.timestamp),
      // color: [255, 255, 0, 0],
      /*
      getLineColor: d => colorToRGBArray(d.properties.color),
      getRadius: d => 100,
      getLineWidth: d => 1,
      getElevation: d => 30,
      onHover: ({object}) => setTooltip(object.properties.name || object.properties.station) */
    });
  });

  return (
    <DeckGL {...viewport} layers={[layers]} />
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
