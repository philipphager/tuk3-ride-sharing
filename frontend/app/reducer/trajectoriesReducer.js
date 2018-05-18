const defaultTrajectoriesState = {
  trejectories: [],
  currentTrajectoryId: null,
  trajectoryData: null,
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
      };
    default:
      return state;
  }
}
