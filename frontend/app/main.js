import React from 'react';
import ReactDOM from 'react-dom';
import { AppContainer } from 'react-hot-loader';
import { createStore, applyMiddleware, compose } from 'redux';
import reduxThunk from 'redux-thunk';
import { Provider } from 'react-redux';

import reducer from './reducer';
import Root from './config/Root';
// eslint-disable-next-line
const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const store = createStore(reducer, {}, composeEnhancers(applyMiddleware(reduxThunk)));

const render = (Component) => {
  ReactDOM.render(
    <AppContainer>
      <Provider store={store}>
        <Component />
      </Provider>
    </AppContainer>,
    document.getElementById('root'),
  );
};

render(Root);

if (module.hot) {
  module.hot.accept('./config/Root', () => {
    const newApp = require('./config/Root').default;
    render(newApp);
  });
}
