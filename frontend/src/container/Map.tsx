import * as React from 'react';
// @ts-ignore
import Dimensions from 'react-dimensions';
import ReactMapGL from 'react-map-gl';
import { connect } from 'react-redux';
import DeckGlLayer from '../components/DeckGLLayer';
import { IStoreState } from '../types';

export interface Props {
    containerWidth: number;
    containerHeight: number;
    trajectoryData: any[];
}

class Map extends React.Component<Props, any> {
    constructor(props: any) {
        super(props);
        this.state = {
            viewport: {
                width: this.props.containerWidth,
                height: 800,
                latitude: 22.543099,
                longitude: 114.057868,
                zoom: 8
            }
        }
    }

    public render() {
        const colors = [
            [255, 139, 139, 255],
            [97, 191, 173, 255],
            [15, 207, 97, 255],
            [55, 23, 34, 255],
            [27, 29, 28, 255],
            [119, 238, 223, 255],
        ];
        const data = this.props.trajectoryData.map((trajData, index) => {
            return {
                type: trajData.type,
                properties: {
                    color: colors[index],
                    ...trajData.properties,
                },
                geometry: {
                // eslint-disable-next-line
                    coordinates: trajData.geometry.coordinates,
                    type: trajData.geometry.type,
                },
            };
        });

        console.log(data);

        return (
            <ReactMapGL
                {...this.state.viewport}
                mapboxApiAccessToken={process.env.REACT_APP_MAPBOX_ACCESS_TOKEN}
                mapStyle={process.env.REACT_APP_MAPBOX_STYLE}
                onViewportChange={this.handleViewportChange}
            >
                {data.length ? <DeckGlLayer
                    data={data}
                    viewport={this.state.viewport}
                /> : null}
            </ReactMapGL>
        );
    }

    private handleViewportChange = (newViewport: object) => {
        this.setState({
            viewport: newViewport
        })
    }
}

function mapStateToProps({ map }: IStoreState) {
    return {
        trajectoryData: map.trajectoryData
    }
}

export default Dimensions()(connect(mapStateToProps)(Map));
