/* eslint-disable */
import DeckGL, { GeoJsonLayer } from 'deck.gl';
import PropTypes from 'prop-types';
import * as React from 'react';
/* eslint-enable */

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

/* eslint-enable */

export default DeckGlLayer;
