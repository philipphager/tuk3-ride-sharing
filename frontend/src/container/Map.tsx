import { Col, Row, Slider } from 'antd';
// @ts-ignore
import hashColor from 'hash-color-material';
// @ts-ignore
import hexRgb from 'hex-rgb';
// @ts-ignore
import * as TimeFormat from 'hh-mm-ss';
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
            opacity: 100
        }
    }

    public render() {
        const data = this.props.trajectoryData.map((trajData: any, index: number) => {
            console.log(trajData.properties.trip_id);
            const trajColor = hexRgb(hashColor.getColorFromString(String(trajData.properties.trip_id)), {format: 'array'});

            if (index > 0){
                trajColor[3] = this.state.opacity;
            }
            console.table(trajColor);
            return {
                type: trajData.type,
                properties: {
                    color: trajColor,
                    ...trajData.properties,
                },
                geometry: {
                // eslint-disable-next-line
                    coordinates: trajData.geometry.coordinates,
                    type: trajData.geometry.type,
                },
            };
        });

        const trajectoryInformation: JSX.Element = (<Row gutter={18}>
            <Col span={4}>
                Duration: {this.state.tootipData ? TimeFormat.fromS(this.state.tootipData.duration_time, 'hh:mm:ss') : '-'}
            </Col>
            <Col span={4}>
                Start: {this.state.tootipData ? TimeFormat.fromS(this.state.tootipData.start_time, 'hh:mm:ss') : '-'}
            </Col>
            <Col span={4}>
                End: {this.state.tootipData ? TimeFormat.fromS(this.state.tootipData.end_time, 'hh:mm:ss') : '-'}
            </Col>
        </Row>);


        return (
            <React.Fragment>
                <div className="mapInfo">
                    {trajectoryInformation}
                </div>
                <div className="mapMenu">
                    <Slider
                        className="opacitiySlider"
                        value={this.state.opacity}
                        onChange={this.handleOpacityChange}
                        min={0}
                        max={255}
                    />
                </div>
                <ReactMapGL id="map" className="mapGl"
                    {...this.state.viewport}
                    mapboxApiAccessToken={process.env.REACT_APP_MAPBOX_ACCESS_TOKEN}
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

    private handleOpacityChange = (value: any) => {
        this.setState({
            opacity: value
        })
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
