const defaultMapState = {
  viewport: {
    height: 100,
    width: 100,
    latitude: 22.5473063,
    longitude: 114.0453752,
    zoom: 12,
  },
};

export default function (state = defaultMapState, action) {
  switch (action.type) {
    case 'VIEWPORT_CHANGE':
      return {
        viewport: action.viewport,
      };
    case 'CONTAINER_CHANGE':
      return {
        viewport: {
          ...state.viewport,
          width: action.width,
          height: action.height,
        },
      };
    default:
      return state;
  }
}
