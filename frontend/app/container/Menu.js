import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Row, Col, Slider, Spin } from 'antd';

import * as actions from '../actions/trajectoryActions';
import TrajectorySelect from '../components/TrajectorySelect';

class Menu extends Component {
  static propTypes = {
    getTrajectories: PropTypes.func.isRequired,
    getTrajectory: PropTypes.func.isRequired,
    changeMaxTrajectoryFrame: PropTypes.func.isRequired,
    trajectoryIds: PropTypes.arrayOf(PropTypes.number),
  }

  static defaultProps = {
    trajectoryIds: null,
  }

  componentWillMount = () => {
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
      <Row>
        <Col span={6}>
          Trajectory Id:
          {this.props.trajectoryIds ? (
            <TrajectorySelect
              options={this.props.trajectoryIds.slice(0, 100)}
              onChange={this.props.getTrajectory}
            />
          ) : (
            <Spin />
          )}
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
    );
  }
}

function mapStateToProps({ trajectories }) {
  return {
    trajectoryIds: trajectories.trejectoryIds,
  };
}

export default connect(mapStateToProps, actions)(Menu);
