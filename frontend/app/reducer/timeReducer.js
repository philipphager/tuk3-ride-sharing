const defaultTimeState = {
  times: {
    frame_trajectory: {
      FETCH_TRAJECTORIES: [],
      FETCH_TRAJECTORY: [],
    },
    point_trajectory: {
      FETCH_TRAJECTORIES: [],
      FETCH_TRAJECTORY: [],
    },
  },
};

export default function (state = defaultTimeState, action) {
  switch (action.type) {
    case 'ADD_TIME': {
      const newTimes = state.times;
      newTimes[action.format][action.actionType] = [
        ...newTimes[action.format][action.actionType],
        action.time,
      ];
      return {
        ...state,
        times: newTimes,
      };
    }
    default:
      return state;
  }
}
