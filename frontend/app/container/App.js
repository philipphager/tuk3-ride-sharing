import React, { Component, Fragment } from 'react';
import 'antd/dist/antd.css';
import { Row } from 'antd';
import ResizableMap from './Map';
import Menu from './Menu';

class App extends Component {
  render() {
    return (
      <Fragment>
        <Row>
          <div style={{ width: '100vw', height: '80vh' }}>
            <ResizableMap />
          </div>
        </Row>
        <Row>
          <Menu />
        </Row>
      </Fragment>
    );
  }
}

export default App;
