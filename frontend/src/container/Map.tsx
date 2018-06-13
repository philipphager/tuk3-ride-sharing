import * as React from 'react';
// @ts-ignore
import Dimensions from 'react-dimensions';
import ReactMapGL from 'react-map-gl';

export interface Props {
    containerWidth: number;
    containerHeight: number;
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
        return (
            <ReactMapGL
                {...this.state.viewport}
                mapboxApiAccessToken={process.env.REACT_APP_MAPBOX_ACCESS_TOKEN}
                mapStyle={process.env.REACT_APP_MAPBOX_STYLE}
                onViewportChange={this.handleViewportChange}
            />
        );
    }

    private handleViewportChange = (newViewport: object) => {
        this.setState({
            viewport: newViewport
        })
    }
}

export default Dimensions()(Map);
