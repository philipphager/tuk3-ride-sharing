const defaultTrajectoriesState = {
  isFetching: false,
  maxFrame: 2880,
  trejectoryIds: [],
  selectedTrajectories: [],
  trajectoriesData: [],
};

export default function (state = defaultTrajectoriesState, action) {
  switch (action.type) {
    case 'FETCH_TRAJECTORIES':
      return {
        ...state,
        trejectoryIds: action.trajectories,
      };
    case 'FETCH_TRAJECTORY':
      return {
        ...state,
        selectedTrajectories: [
          ...state.selectedTrajectories,
          action.selectedTrajectory,
        ],
        trajectoriesData: [
          ...state.trajectoriesData,
          action.trajectoryData,
        ],
        isFetching: false,
      };
    case 'START_FETCHING_TRAJECTORY':
      return {
        ...state,
        isFetching: true,
      };
    case 'REMOVE_TRAJECTORY': {
      const index = state.selectedTrajectories.indexOf(action.trajectoryId);
      return {
        ...state,
        selectedTrajectories: [
          ...state.selectedTrajectories.slice(0, index),
          ...state.selectedTrajectories.slice(index + 1),
        ],
        trajectoriesData: [
          ...state.trajectoriesData.slice(0, index),
          ...state.trajectoriesData.slice(index + 1),
        ],
      };
    }
    case 'CHANGE_MAX_FRAME':
      return {
        ...state,
        maxFrame: action.maxFrame,
      };
    default:
      return state;
  }
}
