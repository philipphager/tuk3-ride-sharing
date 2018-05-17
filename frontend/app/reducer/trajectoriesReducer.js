const defaultTrajectoriesState = {
  trejectories: [],
};

export default function (state = defaultTrajectoriesState, action) {
  switch (action.type) {
    case 'FETCH_TRAJECTORIES':
      return {
        trajectories: action.trajectories,
      };
    default:
      return state;
  }
}
