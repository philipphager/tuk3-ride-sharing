/* eslint-disable */
export const changeViewport = (viewport) => dispatch => {
  dispatch({
    type: 'VIEWPORT_CHANGE',
    viewport: viewport
  });
};

export const changeContainerSize = (width, height) => dispatch => {
  dispatch({
    type: 'CONTAINER_CHANGE',
    width: width,
    height: height,
  });
};
