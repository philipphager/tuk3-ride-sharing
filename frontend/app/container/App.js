import React, { Component, Fragment } from 'react';
import PropTypes from 'prop-types';
import 'antd/dist/antd.css';
import { connect } from 'react-redux';
import { Row, Col, Spin, Slider } from 'antd';
import ResizableMap from './Map';
import TrajectorySelect from '../components/TrajectorySelect';
import * as actions from '../actions/trajectoryActions';

class App extends Component {
  static propTypes = {
    getTrajectories: PropTypes.func.isRequired,
    getTrajectory: PropTypes.func.isRequired,
    changeMaxTrajectoryFrame: PropTypes.func.isRequired,
    trejectoryIds: PropTypes.arrayOf(PropTypes.number),
  }

  componentDidMount = () => {
    this.props.getTrajectories();
  }

  handleTimeChange = (newValue) => {
    this.props.changeMaxTrajectoryFrame(newValue);
  }

  handleFormat = (value) => {
    const hour = (`0${Math.floor(value / 120)}`).slice(-2);
    const minute = (`0${Math.floor((value / 2) - (60 * hour))}`).slice(-2);
    return `${hour}:${minute}`;
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
          <Col span={16}>
            <Slider
              min={0}
              defaultValue={2880}
              max={2880}
              onChange={this.handleTimeChange}
              tipFormatter={this.handleFormat}
            />
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
