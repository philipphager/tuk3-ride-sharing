export const CHANGE_DATA_FORMAT = 'CHANGE_DATA_FORMAT';
export type CHANGE_DATA_FORMAT = typeof CHANGE_DATA_FORMAT;

export enum DataFormats {
    PointTrip = "point-trip",
    FrameTrip = "frame-trip",
    KeyTrip = "key-trip",
}

export type DataFormat = typeof DataFormats;

export const ADD_TRAJECTORY_DATA = 'ADD_TRAJECTORY_DATA';
export type ADD_TRAJECTORY_DATA = typeof ADD_TRAJECTORY_DATA;

export const RESET_TRAJECTORY_DATA = 'RESET_TRAJECTORY_DATA';
export type RESET_TRAJECTORY_DATA = typeof RESET_TRAJECTORY_DATA;
