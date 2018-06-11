import { combineReducers } from 'redux';
import mapReducer from './mapReducer';
import trajectoriesReducer from './trajectoriesReducer';
import timeReducer from './timeReducer';

export default combineReducers({
  map: mapReducer,
  trajectories: trajectoriesReducer,
  time: timeReducer,
});
