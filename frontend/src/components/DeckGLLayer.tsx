// @ts-ignore
import DeckGL, { GeoJsonLayer } from 'deck.gl';
import * as React from 'react';

const DeckGlLayer = ({ data, viewport, onHover}: any) => {
    const layers = data.map((trajectoryData: any, index: number) => {
        return new GeoJsonLayer({
            id: index,
            data: trajectoryData,
            pickable: true,
            stroked: false,
            filled: true,
            extruded: true,
            lineWidthScale: 12,
            lineWidthMinPixels: 4,
            getLineColor: (d: any) => d.properties.color,
            onHover: ({ object }: any) => {
                if (object) {
                    onHover(object.properties);
                }
            }
        });
    });

    return (
        <DeckGL {...viewport} layers={[layers]} />
    );
};

/* eslint-enable */

export default DeckGlLayer;
