import { MapAction } from "../actions";
import { ADD_TRAJECTORY_DATA, NEW_RIDE_SHARING, RESET_TRAJECTORY_DATA } from "../constants";
import { IMapState } from "../types";

const initialState: IMapState = {
  trajectoryData: [],
}

export function map(state: IMapState = initialState, action: MapAction) {
  switch (action.type) {
    case ADD_TRAJECTORY_DATA:
      return {
        ...state,
        trajectoryData: [
          ...state.trajectoryData,
          action.trajectoryData
        ]
      }
    case RESET_TRAJECTORY_DATA:
      return {
        ...state,
        trajectoryData: []
      }
    case NEW_RIDE_SHARING:
      return {
        ...state,
        trajectoryData: [state.trajectoryData[0]]
      }
    default:
      return state;
  }
}
