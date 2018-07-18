import { Button, Col, message, Row, Select, Slider, TimePicker } from "antd";
import axios from 'axios';
// @ts-ignore
import * as TimeFormat from 'hh-mm-ss';
import * as moment from 'moment';
import { Moment } from "moment";
import * as React from "react";
import { connect, Dispatch } from "react-redux";
import * as actions from '../actions';
import { DataFormats } from "../constants";
import { IStoreState } from "../types";
import './Menu.css';

interface Props {
    dataFormat: DataFormats;
    onDataFrameChange: (x: DataFormats) => void;
    addTrajectoryData: (x: any) => void;
    resetTrajectoryData: () => void;
    newRideSharing: () => void;
}

interface State {
    trajectoryTime: Moment;
    trajectoryIds: number[];
    selectedTrajectories: number[];
    selectedTime: number;
    selectedTripId: number;
    distance: number;
    isLoading: boolean;
    numberOfTrips: number;
    time: number;
    alreadyFetched: boolean;
    endpoint: 'point-ride-sharing' | 'key-ride-sharing' | 'frame-ride-sharing' ;
}

class Menu extends React.Component<Props, State> {
    constructor(props: Props) {
        super(props);
        this.state = {
            trajectoryTime: moment(),
            trajectoryIds: [],
            selectedTrajectories: [],
            selectedTime: 43250,
            selectedTripId: 22248000,
            distance: 10,
            isLoading: false,
            numberOfTrips: 0,
            time: 60,
            alreadyFetched: false,
            endpoint: 'point-ride-sharing'
        }
    }

    public componentDidMount() {
        // get the trajectory ids
        axios.get(`/${this.props.dataFormat}/?limit=1000&offset=0`)
            .then(response => {
                this.setState({
                    trajectoryIds: response.data.data.trip_ids
                })
            })
    }

    public render() {
        const selectTrajectoryIdsOptions: JSX.Element[] = this.state.trajectoryIds.map((value: number) =>
            (<Select.Option key={value} value={value}>{value}</Select.Option>)
        );


        return (
            <Row className="menuBar" gutter={24} justify="center" type="flex" align="middle">
                <Col span={4}>
                    <Row className="menuInfo">Endpoint</Row>
                    <Row>
                        <Select value={this.state.endpoint} onChange={this.onChangeEndpoint}>
                            <Select.Option value='point-ride-sharing'>Point</Select.Option>
                            <Select.Option value='key-ride-sharing'>Key</Select.Option>
                            <Select.Option value='frame-ride-sharing'>Frame</Select.Option>
                        </Select>
                    </Row>
                </Col>
                <Col span={4}>
                    <Row className="menuInfo">
                        Time of Day
                    </Row>
                    <Row>
                        <TimePicker onChange={this.onTimeChange} value={this.state.trajectoryTime} />
                    </Row>
                </Col>
                <Col span={3}>
                    <Row className="menuInfo">
                        Base-Trajectory ID
                    </Row>
                    <Row>
                        <Select size="default" style={{ width: '100px'}} value={this.state.selectedTripId} placeholder="Select Trajectory Id" onSelect={this.onTrajectorySelect}>
                            {selectTrajectoryIdsOptions}
                        </Select>
                    </Row>
                </Col>
                <Col span={5}>
                    <Row className="menuInfo">
                        Max Distance
                    </Row>
                    <Row>
                        <Slider
                            className="distanceSlider"
                            min={0}
                            max={1000}
                            step={1}
                            value={this.state.distance}
                            onChange={this.handleDistanceChange}
                            tipFormatter={this.formatTipMeter}
                        />
                    </Row>
                </Col>
                <Col span={5}>
                    <Row className="menuInfo">
                        Time Distance
                    </Row>
                    <Row>
                        <Slider
                            className="timeSlider"
                            min={1} max={900}
                            value={this.state.time}
                            step={1}
                            onChange={this.handleTimeChange}
                            tipFormatter={this.formatTip}
                        />
                    </Row>
                </Col>
                <Col span={2}>
                    <Button loading={this.state.isLoading} onClick={this.handleRideSharingRequest} disabled={!this.state.alreadyFetched}>Search</Button>
                </Col>
                <Col span={4}>
                    Number of Trips: {this.state.numberOfTrips}
                </Col>
            </Row>
        );
    }

    private onChangeEndpoint = (value: any) => {
        this.setState({
            endpoint: value
        })
    }

    private formatTipMeter = (value: any) => {
        return value + ' meter'
    }

    private formatTip = (value: any) => {
        return TimeFormat.fromS(value, 'mm:ss') + ' minutes'
    }

    private onTimeChange = (value: Moment) => {
        this.setState({
            trajectoryTime: value
        })
        const seconds: number = value.diff(moment().startOf('day'), 'seconds');
        axios.get(`/${this.props.dataFormat}/?limit=1000&offset=0&time=${seconds}`)
            .then(response => {
                console.log(response);
                this.setState({
                    trajectoryIds: response.data.data.trip_ids
                })
            })
    }

    private handleDistanceChange = (value: any): void => {
        this.setState({
            distance: value
        })
    }

    private handleTimeChange = (value: any): void => {
        this.setState({
            time: value
        })
    }

    private handleRideSharingRequest = (): void => {
        this.props.newRideSharing();
        this.setState({ isLoading: true });
        axios.get(`/${this.state.endpoint}/${this.state.selectedTripId}?distance=${this.state.distance}&time=${this.state.time}`)
            .then(response => {
                if(response.data.data && response.data.data.length > 0) {
                    console.log(response.data.data);
                    response.data.data.forEach((trajectory: any) => {
                        this.props.addTrajectoryData(trajectory);
                    });
                }
                this.setState({
                    isLoading: false,
                    numberOfTrips: response.data.data.length
                });
            })
            .catch((reason: any) => {
                message.error('Failed to load similary trips');
                this.setState({
                    isLoading: false
                });
            })
    }

    private onTrajectorySelect = (value: number): void => {
        this.props.resetTrajectoryData();
        this.setState({
            selectedTripId: value,
            alreadyFetched: true
        });
        axios.get(`/point-trip/${value}`)
            .then((response: any) => {
                console.log(response.data.data);
                this.props.addTrajectoryData(response.data.data);
            })
    }
}

export function mapSateToProps({ settings }: IStoreState) {
    return {
        dataFormat: settings.dataFormat
    }
}

export function mapDispatchToProps(dispatch: Dispatch<actions.MenuAction>) {
    return {
        onDataFrameChange: (newDataFormat: DataFormats) => {
            dispatch(actions.changeDataFormat(newDataFormat))
        },
        addTrajectoryData: (data: any) => {
            dispatch(actions.addTrajectoryData(data))
        },
        resetTrajectoryData: () => {
            dispatch(actions.resetTrajectoryData())
        },
        newRideSharing: () => {
            dispatch(actions.newRideSharing())
        }
    }
}

export default connect(mapSateToProps, mapDispatchToProps)(Menu);
