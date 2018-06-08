import { Select } from "antd";
import * as React from "react";
import { connect, Dispatch } from "react-redux";
import * as actions from '../actions';
import { DataFormats } from "../constants";
import { ISettingsState } from "../types";

export interface Props {
    dataFormat: DataFormats,
    onDataFrameChange: (x: DataFormats) => void;
}

class Menu extends React.Component<Props, object> {
    constructor(props: Props) {
        super(props);
    }

    public render() {
        const selectItems: any[] = Object.keys(DataFormats).map(value =>
            (<Select.Option key={value}>{value}</Select.Option>)
        );
        return (
            <Select size="default" value={this.props.dataFormat} onChange={ this.onDatFormChange }>
                {selectItems}
            </Select>
        );
    }

    private onDatFormChange = (value: DataFormats) => {
        this.props.onDataFrameChange(value);
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
