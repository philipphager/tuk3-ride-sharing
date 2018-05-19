import React, { Component, Fragment } from 'react';
import { Row, Col, Spin } from 'antd';
import PropTypes from 'prop-types';
import 'antd/dist/antd.css';
import { connect } from 'react-redux';
import ResizableMap from './Map';
import TrajectorySelect from '../components/TrajectorySelect';
import * as actions from '../actions/trajectoryActions';

class App extends Component {
  static propTypes = {
    getTrajectories: PropTypes.func.isRequired,
    getTrajectory: PropTypes.func.isRequired,
    trejectoryIds: PropTypes.arrayOf(PropTypes.number),
  }

  componentDidMount = () => {
    this.props.getTrajectories();
  }

  render() {
    return (
      <Fragment>
        <Row>
          <div style={{ width: '100vw', height: '80vh' }}>
            <ResizableMap />
          </div>
        </Row>
        <Row>
          <Col span={6}>
            Trajectory Id:
            { this.props.trejectoryIds ?
              <TrajectorySelect
                options={this.props.trejectoryIds.slice(0, 100)}
                onChange={this.props.getTrajectory}
              />
              : <Spin />}
          </Col>
        </Row>
      </Fragment>
    );
  }
}

function mapStateToProps({ trajectories }) {
  return {
    trejectoryIds: trajectories.trejectoryIds,
  };
}

App.defaultProps = {
  trejectoryIds: [],
};

export default connect(mapStateToProps, actions)(App);
