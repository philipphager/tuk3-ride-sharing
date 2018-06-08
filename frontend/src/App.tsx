import { Layout } from 'antd';
import * as React from 'react';
import './App.css';
import Menu from './container/Menu';

const { Header, Content } = Layout;

const App = () => (
  <React.Fragment>
    <Layout>
      <Header className="Menu"><Menu /></Header>
      <Content>Test</Content>
    </Layout>
  </React.Fragment>
)

export default App;
