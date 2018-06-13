import { Col, Row, Select, Slider, Tag, TimePicker } from "antd";
import * as moment from 'moment';
import * as React from "react";
import { connect, Dispatch } from "react-redux";
import * as actions from '../actions';
import { DataFormats } from "../constants";
import { ISettingsState } from "../types";

import { SliderMarks } from "antd/lib/slider";
import { Moment } from "moment";
import './Menu.css';
export interface Props {
    dataFormat: DataFormats,
    onDataFrameChange: (x: DataFormats) => void;
}

class Menu extends React.Component<Props, any> {
    constructor(props: Props) {
        super(props);
        this.state = {
            isPlaying: false,
            stepSize: 1,
            time: moment(),
        }
    }

    public render() {
        const selectItems: any[] = Object.keys(DataFormats).map(value =>
            (<Select.Option key={value} value={value}>{value}</Select.Option>)
        );

        const marks: SliderMarks = {
            0: '0',
            1440: '12',
            2880: '24'
        }

        return (
            <Row className="menuBar" gutter={24} justify="center" type="flex" align="middle">
                <Col span={4}>
                    <Select size="default" style={{ width: '100px'}} value={this.props.dataFormat} onChange={ this.onDatFormChange }>
                        {selectItems}
                    </Select>
                </Col>
                <Col span={4}>
                    <TimePicker onChange={this.onTimeChange} value={this.state.time} />
                </Col>
                <Col span={4}>
                    <Select size="default" style={{ width: '100px'}} placeholder="Select Trajectory Id">
                        <Select.Option value="test">
                            12345501
                        </Select.Option>
                    </Select>
                </Col>
                <Col span={8}>
                    <Row>
                        Selected IDs:
                        <Tag closable={true}>Test</Tag>
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

    private onDatFormChange = (value: DataFormats) => {
        this.props.onDataFrameChange(value);
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
