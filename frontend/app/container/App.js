import React, { Fragment } from 'react';
import 'antd/dist/antd.css';
import { Row } from 'antd';
import ResizableMap from './Map';
import Menu from './Menu';
import './app.css';

const App = () => {
  return (
    <Fragment>
      <Row>
        <Menu />
      </Row>
      <Row>
        <div style={{ width: '100vw', height: '90vh' }}>
          <ResizableMap />
        </div>
      </Row>
    </Fragment>
  );
};

export default App;
