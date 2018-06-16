import { DataFormats } from "../constants";

export interface ISettingsState {
    dataFormat: DataFormats;
}


export interface IMapState {
    trajectoryData: any[];
}

export interface IStoreState {
    settings: ISettingsState;
    map: IMapState
}
