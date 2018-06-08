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
