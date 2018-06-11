/* eslint-disable */
import axios from 'axios';

export const getTrajectories = (format) => dispatch => {
  axios.get(`/${format}/`)
    .then(function(response){
      dispatch({
        type: 'FETCH_TRAJECTORIES',
        trajectories: response.data.data.trajectory_ids
      });
      dispatch({
        type: 'ADD_TIME',
        time: response.data.time,
        actionType: 'FETCH_TRAJECTORIES',
        format: format.replace('-', '_'),
      })
    });
}

export const getTrajectory = (trajectoryId, format) => dispatch => {
  dispatch({
    type: 'START_FETCHING_TRAJECTORY',
  })
  axios.get(`/${format}/${trajectoryId}`)
    .then(function(response){
      console.log(response.data);
      dispatch({
        type: 'FETCH_TRAJECTORY',
        selectedTrajectory: trajectoryId,
        trajectoryData: {
          trajectoryId: trajectoryId,
          geoJsonData: response.data.data,
        },
      })
      dispatch({
        type: 'ADD_TIME',
        time: response.data.time,
        actionType: 'FETCH_TRAJECTORY',
        format: format.replace('-', '_'),
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
