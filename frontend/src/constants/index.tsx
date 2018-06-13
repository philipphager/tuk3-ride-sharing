export const CHANGE_DATA_FORMAT = 'CHANGE_DATA_FORMAT';
export type CHANGE_DATA_FORMAT = typeof CHANGE_DATA_FORMAT;

export enum DataFormats {
    PointTrip = "point-trip",
    FrameTrip = "frame-trip",
}

export type DataFormat = typeof DataFormats;
