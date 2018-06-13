import { Col, Row, Select, Slider, Tag, TimePicker } from "antd";
import axios from 'axios';
import * as moment from 'moment';
import * as React from "react";
import { connect, Dispatch } from "react-redux";
import * as actions from '../actions';
import { DataFormats } from "../constants";
import { ISettingsState } from "../types";

import { SliderMarks } from "antd/lib/slider";
import { Moment } from "moment";
import './Menu.css';
interface Props {
    dataFormat: DataFormats,
    onDataFrameChange: (x: DataFormats) => void;
}

interface State {
    isPlaying: boolean,
    stepSize: number,
    time: Moment,
    trajectoryIds: number[],
    selectedTrajectories: number[],
}

class Menu extends React.Component<Props, State> {
    constructor(props: Props) {
        super(props);
        this.state = {
            isPlaying: false,
            stepSize: 1,
            time: moment(),
            trajectoryIds: [],
            selectedTrajectories: []
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
        const selectFormatOptions: JSX.Element[] = Object.keys(DataFormats).map(key =>
            (<Select.Option key={key} value={DataFormats[key]}>{key}</Select.Option>)
        );

        const selectTrajectoryIdsOptions: JSX.Element[] = this.state.trajectoryIds.map((value: number) =>
            (<Select.Option key={value} value={value}>{value}</Select.Option>)
        );

        const marks: SliderMarks = {
            0: '0',
            1440: '12',
            2880: '24'
        };

        let trajectoryIdTags: JSX.Element[]= [];
        if (this.state.selectedTrajectories.length > 0) {
            trajectoryIdTags = this.state.selectedTrajectories.map(value => (
                <Tag closable={true} key={value}>{value}</Tag>
            ));
        }

        return (
            <Row className="menuBar" gutter={24} justify="center" type="flex" align="middle">
                <Col span={4}>
                    <Select size="default" style={{ width: '100px'}} value={this.props.dataFormat} onChange={ this.onDatFormChange }>
                        {selectFormatOptions}
                    </Select>
                </Col>
                <Col span={4}>
                    <TimePicker onChange={this.onTimeChange} value={this.state.time} />
                </Col>
                <Col span={4}>
                    <Select size="default" style={{ width: '100px'}} placeholder="Select Trajectory Id" onSelect={this.onTrajectorySelect}>
                        {selectTrajectoryIdsOptions}
                    </Select>
                </Col>
                <Col span={8}>
                    <Row>
                        Selected IDs:
                        {trajectoryIdTags ? trajectoryIdTags : null}
                    </Row>
                    <Row>
                        <Slider
                            min={1}
                            max={2879}
                            marks={marks}
                            tipFormatter={this.handleFormat}
                        />
                    </Row>
                </Col>
            </Row>
        );
    }

    private onTimeChange = (value: Moment) => {
        this.setState({
            time: value,
        })
    }

    private onTrajectorySelect = (value: number) => {
        this.setState({
            selectedTrajectories: [... this.state.selectedTrajectories, value]
        })
    }

    private onDatFormChange = (value: DataFormats) => {
        this.props.onDataFrameChange(value);
        axios.get(`/${value}/?limit=1000&offset=0`)
            .then(response => {
                this.setState({
                    trajectoryIds: response.data.data.trip_ids
                })
            })
    }

    private handleFormat = (value: number): string => {
        const hour: number = Number((`0${Math.floor(value / 120)}`).slice(-2));
        const minute: number = Number((`0${Math.floor((value / 2) - (60 * hour))}`).slice(-2));
        return`${hour}:${minute}`;
    }
}

export function mapSateToProps({ dataFormat }: ISettingsState) {
    return {
        dataFormat
    }
}

export function mapDispatchToProps(dispatch: Dispatch<actions.SettingsAction>) {
    return {
        onDataFrameChange: (newDataFormat: DataFormats) => {
            dispatch(actions.changeDataFormat(newDataFormat))
        },
    }
}

export default connect(mapSateToProps, mapDispatchToProps)(Menu);
