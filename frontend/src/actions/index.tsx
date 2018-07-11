import * as constants from '../constants';

export interface IChangeDataFormat {
    type: constants.CHANGE_DATA_FORMAT;
    dataFormat: constants.DataFormats;
}

export type SettingsAction = IChangeDataFormat;

export function changeDataFormat(inDataFormat: constants.DataFormats): IChangeDataFormat {
    return {
        type: constants.CHANGE_DATA_FORMAT,
        dataFormat: inDataFormat,
    }
}

export interface IAddTrajectoryData {
    type: constants.ADD_TRAJECTORY_DATA;
    trajectoryData: any;
}

export function addTrajectoryData(data: any): IAddTrajectoryData {
    return {
        type: constants.ADD_TRAJECTORY_DATA,
        trajectoryData: data,
    }
}

export interface IResetTrajectoryData {
    type: constants.RESET_TRAJECTORY_DATA
}

export function resetTrajectoryData(): IResetTrajectoryData {
    return {
        type: constants.RESET_TRAJECTORY_DATA
    }
}

export type MapAction = IAddTrajectoryData | IResetTrajectoryData;

export type MenuAction = IChangeDataFormat | IAddTrajectoryData | IResetTrajectoryData;
