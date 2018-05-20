/* eslint-disable */
import axios from 'axios';

export const getTrajectories = () => dispatch => {
  axios.get('/trajectory/')
    .then(function(response){
      dispatch({
        type: 'FETCH_TRAJECTORIES',
        trajectories: response.data.trajectory_ids
      })
    });
}

export const getTrajectory = (trajectoryId) => dispatch => {
  dispatch({
    type: 'START_FETCHING_TRAJECTORY',
  })
  axios.get('/trajectory/' + trajectoryId)
    .then(function(response){
      dispatch({
        type: 'FETCH_TRAJECTORY',
        selectedTrajectory: trajectoryId,
        trajectoryData: {
          trajectoryId: trajectoryId,
          geoJsonData: response.data,
        },
      })
    });
}

export const removeTrajectory = (trajectoryId) => dispatch => {
  dispatch({
    type: 'REMOVE_TRAJECTORY',
    trajectoryId: trajectoryId,
  });
}

export const changeMaxTrajectoryFrame = (maxFrame) => dispatch => {
  dispatch({
    type: 'CHANGE_MAX_FRAME',
    maxFrame: maxFrame,
  });
}
