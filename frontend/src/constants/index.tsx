export const CHANGE_DATA_FORMAT = 'CHANGE_DATA_FORMAT';
export type CHANGE_DATA_FORMAT = typeof CHANGE_DATA_FORMAT;

export enum DataFormats {
    PointTrajectory = "point-trajectory",
    FrameTrajectory = "frame-trajectory",
}

export type DataFormat = typeof DataFormats;
