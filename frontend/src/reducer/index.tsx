import { combineReducers } from "redux";
import { map } from './mapReducer';
import { settings } from './settingsReducer';

export default combineReducers({
  settings,
  map
})
