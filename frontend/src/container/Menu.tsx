import { Col, Row, Select, Slider, Tag, TimePicker } from "antd";
import { Button } from "antd/lib/radio";
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
    isPlaying: boolean;
    stepSize: number;
    trajectoryTime: Moment;
    sliderTime: number;
    trajectoryIds: number[];
    selectedTrajectories: number[];
    selectedTime: number;
}

class Menu extends React.Component<Props, State> {
    constructor(props: Props) {
        super(props);
        this.state = {
            isPlaying: false,
            stepSize: 1,
            trajectoryTime: moment(),
            sliderTime: 43250,
            trajectoryIds: [],
            selectedTrajectories: [],
            selectedTime: 43250,
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

        let trajectoryIdTags: JSX.Element[]= [];
        if (this.state.selectedTrajectories.length > 0) {
            trajectoryIdTags = this.state.selectedTrajectories.map(value => (
                <Tag closable={true} afterClose={() => this.handleTagClose(value)} key={value}>{value}</Tag>
            ));
        }

        return (
            <Row className="menuBar" gutter={24} justify="center" type="flex" align="middle">
                <Col span={4}>
                    <TimePicker onChange={this.onTimeChange} value={this.state.trajectoryTime} />
                </Col>
                <Col span={3}>
                    <Select size="default" style={{ width: '100px'}} placeholder="Select Trajectory Id" onSelect={this.onTrajectorySelect}>
                        {selectTrajectoryIdsOptions}
                    </Select>
                </Col>
                <Col span={2}>
                    <Slider className="distanceSlider" min={0} max={100} step={0.01}/>
                </Col>
                <Col span={2}>
                    <Button>Run</Button>
                </Col>
                <Col span={8}>
                    <Row>
                        {trajectoryIdTags ? trajectoryIdTags : null}
                    </Row>
                </Col>
            </Row>
        );
    }

    private onTimeChange = (value: Moment) => {
        this.setState({
            trajectoryTime: value,
        })
    }

    private onTrajectorySelect = (value: number): void => {
        if(this.state.selectedTrajectories.indexOf(value) === -1) {
            this.setState({
                selectedTrajectories: [... this.state.selectedTrajectories, value]
            });
        }
        axios.get(`/${this.props.dataFormat}/${value}?max_time=${this.state.selectedTime}`)
            .then(response => {
                this.props.addTrajectoryData(response.data.data);
            })
    }

    private handleTagClose = (value: number): void => {
        const indexRemoveTag = this.state.selectedTrajectories.indexOf(value);
        const newTrajectoryIDs = [
            ...this.state.selectedTrajectories.slice(0, indexRemoveTag),
            ...this.state.selectedTrajectories.slice(indexRemoveTag + 1)
        ]
        this.setState({
            selectedTrajectories: newTrajectoryIDs
        })
        this.handleTrajectoryUpdate();
    }

    private handleTrajectoryUpdate = (): void => {
        this.state.selectedTrajectories.forEach(value => {
            axios.get(`/${this.props.dataFormat}/${value}?max_time=${this.state.selectedTime}`)
            .then(response => {
                this.props.addTrajectoryData(response.data.data);
            })
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
