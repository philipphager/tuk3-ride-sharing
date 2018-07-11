import { Row } from 'antd';
import * as React from 'react';
import './App.css';
import Map from './container/Map';
import Menu from './container/Menu';

const App = () => (
  <React.Fragment>
    <Menu />
    <Row>
      <Map />
    </Row>
  </React.Fragment>
)

export default App;
