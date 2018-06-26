import { Col, Row } from 'antd';
// @ts-ignore
import hashColor from 'hash-color-material';
// @ts-ignore
import hexRgb from 'hex-rgb';
import * as React from 'react';
// @ts-ignore
import Dimensions from 'react-dimensions';
import ReactMapGL from 'react-map-gl';
// @ts-ignore
import { connect } from 'react-redux';
import DeckGlLayer from '../components/DeckGLLayer';
import { IStoreState } from '../types';

import './Map.css';

export interface Props {
    containerWidth: number;
    containerHeight: number;
    trajectoryData: any[];
    isTooltipActive: boolean;
    tootipData: any;
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
                zoom: 10
            },
            isTooltipActive: false,
            tootipData: null,
        }
    }

    public render() {
        const data = this.props.trajectoryData.map((trajData: any) => {
            console.log(trajData.properties.trip_id);
            return {
                type: trajData.type,
                properties: {
                    color: hexRgb(hashColor.getColorFromString(String(trajData.properties.trip_id)), {format: 'array'}),
                    ...trajData.properties,
                },
                geometry: {
                // eslint-disable-next-line
                    coordinates: trajData.geometry.coordinates,
                    type: trajData.geometry.type,
                },
            };
        });

        const trajectoryInformation: JSX.Element = (<Row gutter={12}>
            <Col span={4}>
                Duration: {this.state.tootipData ? this.state.tootipData.duration_time : null}
            </Col>
            <Col span={4}>
                Start: {this.state.tootipData ? this.state.tootipData.start_time : null}
            </Col>
            <Col span={4}>
                End: {this.state.tootipData ? this.state.tootipData.end_time : null}
            </Col>
        </Row>);


        return (
            <React.Fragment>
                <div className="mapInfo">
                    {trajectoryInformation}
                </div>
                <ReactMapGL id="map"
                    {...this.state.viewport}
                    mapboxApiAccessToken={process.env.REACT_APP_MAPBOX_ACCESS_TOKEN}
                    // mapStyle={process.env.REACT_APP_MAPBOX_STYLE}
                    onViewportChange={this.handleViewportChange}
                >
                    {data.length ? <DeckGlLayer
                        data={data}
                        viewport={this.state.viewport}
                        onHover={this.onHover}
                    /> : null}
                </ReactMapGL>
            </React.Fragment>

        );
    }

    private onHover = (data: any) => {
        this.setState({
            isTooltipActive: true,
            tootipData: data
        })
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
