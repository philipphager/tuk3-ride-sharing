import { combineReducers } from 'redux';
import mapReducer from './mapReducer';
import trajectoriesReducer from './trajectoriesReducer';

export default combineReducers({
  map: mapReducer,
  trajectories: trajectoriesReducer,
});
