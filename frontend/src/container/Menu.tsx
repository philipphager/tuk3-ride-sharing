import { Button, Col, Row, Select, Slider, TimePicker } from "antd";
import axios from 'axios';
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
}

interface State {
    trajectoryTime: Moment;
    trajectoryIds: number[];
    selectedTrajectories: number[];
    selectedTime: number;
    selectedTripId: number;
    distance: number;
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
            distance: 10
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
                    <TimePicker onChange={this.onTimeChange} value={this.state.trajectoryTime} />
                </Col>
                <Col span={3}>
                    <Select size="default" style={{ width: '100px'}} value={this.state.selectedTripId} placeholder="Select Trajectory Id" onSelect={this.onTrajectorySelect}>
                        {selectTrajectoryIdsOptions}
                    </Select>
                </Col>
                <Col span={5}>
                    <Slider className="distanceSlider" min={0} max={1000} step={1} onChange={this.handleDistanceChange}/>
                </Col>
                <Col span={2}>
                    <Button onClick={this.handleRideSharingRequest}>Run</Button>
                </Col>
            </Row>
        );
    }

    private onTimeChange = (value: Moment) => {
        this.setState({
            trajectoryTime: value
        })
    }

    private handleDistanceChange = (value: any): void => {
        this.setState({
            distance: value
        })
    }

    private handleRideSharingRequest = (): void => {
        axios.get(`/ride-sharing/${this.state.selectedTripId}?distance=${this.state.distance}`)
            .then(response => {
                if(response.data && response.data.length > 0) {
                    console.log(response.data);
                    response.data.forEach((trajectory: any) => {
                        this.props.addTrajectoryData(trajectory);
                    });
                }
            })
    }

    private onTrajectorySelect = (value: number): void => {
        this.setState({
            selectedTripId: value
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
        }
    }
}

export default connect(mapSateToProps, mapDispatchToProps)(Menu);
