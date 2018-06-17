import { notification } from 'antd';
// @ts-ignore
import DeckGL, { GeoJsonLayer } from 'deck.gl';
import * as React from 'react';

const DeckGlLayer = ({ data, viewport }: any) => {
    const layers = data.map((trajectoryData: any, index: number) => {
        return new GeoJsonLayer({
            id: index,
            data: trajectoryData,
            pickable: true,
            stroked: false,
            filled: true,
            extruded: true,
            lineWidthScale: 10,
            lineWidthMinPixels: 2,
            getLineColor: (d: any) => d.properties.color,
            onHover: () => notification.open({
                message: 'Trajectory Information',
                description: 'as'
            })
        });
    });

    return (
        <DeckGL {...viewport} layers={[layers]} />
    );
};

/* eslint-enable */

export default DeckGlLayer;
