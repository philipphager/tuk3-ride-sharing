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