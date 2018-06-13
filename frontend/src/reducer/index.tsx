import { SettingsAction } from "../actions";
import { CHANGE_DATA_FORMAT, DataFormats } from "../constants";
import { ISettingsState } from "../types";

const initialState: ISettingsState = {
    dataFormat: DataFormats.PointTrip
}

export function settings(state: ISettingsState= initialState, action: SettingsAction): ISettingsState {
    switch (action.type) {
        case CHANGE_DATA_FORMAT:
            return {
                ...state,
                dataFormat: action.dataFormat,
            };
        default:
            return state;
    }
}
