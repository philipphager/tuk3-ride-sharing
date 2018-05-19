const defaultTrajectoriesState = {
  trejectories: [],
  currentTrajectoryId: null,
  trajectoryData: null,
  isFetching: false,
};

export default function (state = defaultTrajectoriesState, action) {
  switch (action.type) {
    case 'FETCH_TRAJECTORIES':
      return {
        trajectories: action.trajectories,
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
    default:
      return state;
  }
}
