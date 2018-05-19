const defaultTrajectoriesState = {
  trejectoryIds: [],
  currentTrajectoryId: null,
  trajectoryData: null,
  isFetching: false,
  maxFrame: 2880,
};

export default function (state = defaultTrajectoriesState, action) {
  switch (action.type) {
    case 'FETCH_TRAJECTORIES':
      return {
        trejectoryIds: action.trajectories,
      };
    case 'FETCH_TRAJECTORY':
      return {
        ...state,
        currentTrajectoryId: action.newTrajectoryID,
        trajectoryData: action.trajectory,
        isFetching: false,
      };
    case 'START_FETCHING_TRAJECTORY':
      return {
        ...state,
        isFetching: true,
      };
    case 'CHANGE_MAX_FRAME':
      return {
        ...state,
        maxFrame: action.maxFrame,
      };
    default:
      return state;
  }
}
