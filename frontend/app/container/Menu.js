import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Row, Col, Slider, Spin, Button } from 'antd';

import * as actions from '../actions/trajectoryActions';
import TrajectorySelect from '../components/TrajectorySelect';

class Menu extends Component {
  static propTypes = {
    getTrajectories: PropTypes.func.isRequired,
    getTrajectory: PropTypes.func.isRequired,
    changeMaxTrajectoryFrame: PropTypes.func.isRequired,
    trajectoryIds: PropTypes.arrayOf(PropTypes.number),
    maxFrame: PropTypes.number,
  }

  static defaultProps = {
    trajectoryIds: null,
    maxFrame: 0,
  }

  constructor(props) {
    super(props);
    this.state = {
      isPlaying: false,
      stepSize: 1,
    };
  }

  componentWillMount() {
    this.props.getTrajectories();
  }

  componentDidMount() {
    this.timerID = setInterval(
      () => {
        if (this.state.isPlaying) {
          this.playingTick();
        }
      },
      10,
    );
  }

  componentWillUnmount() {
    clearInterval(this.timerID);
  }

  handleTimeChange = (newValue) => {
    this.props.changeMaxTrajectoryFrame(newValue);
  }

  playingTick = () => {
    this.props.changeMaxTrajectoryFrame(this.props.maxFrame + this.state.stepSize);
  }

  handleStepSizeChange = (value) => {
    this.setState({ stepSize: value });
  }

  handleFormat = (value) => {
    const hour = (`0${Math.floor(value / 120)}`).slice(-2);
    const minute = (`0${Math.floor((value / 2) - (60 * hour))}`).slice(-2);
    return `${hour}:${minute}`;
  }

  handlePlay = () => {
    this.setState({ isPlaying: !this.state.isPlaying });
  }

  render() {
    return (
      <div className="menu">
        <Row>
          <Col span={3}>
            <Row>
              <span className="menuInfo">Trajectory Id:</span>
            </Row>
            <Row>
              {this.props.trajectoryIds ? (
                <TrajectorySelect
                  options={this.props.trajectoryIds.slice(0, 100)}
                  onChange={this.props.getTrajectory}
                />
              ) : (
                <Spin />
              )}
            </Row>
          </Col>
          <Col span={4}>
            <Row>
              <Col span={4} />
              <Col span={20}>
                <span className="menuInfo">Playing Speed</span>
              </Col>
            </Row>
            <Row>
              <Col span={4}>
                <Button
                  type="primary"
                  icon={this.state.isPlaying ? 'pause' : 'caret-right'}
                  onClick={this.handlePlay}
                />
              </Col>
              <Col span={20}>
                <Slider
                  min={1}
                  max={20}
                  value={this.state.stepSize}
                  onChange={this.handleStepSizeChange}
                />
              </Col>
            </Row>
          </Col>
          <Col span={12}>
            <Row>
              <span className="menuInfo">Control the time of day</span>
            </Row>
            <Row>
              <Slider
                min={0}
                value={this.props.maxFrame}
                max={2880}
                onChange={this.handleTimeChange}
                tipFormatter={this.handleFormat}
              />
            </Row>
          </Col>
        </Row>
      </div>
    );
  }
}

function mapStateToProps({ trajectories }) {
  return {
    trajectoryIds: trajectories.trejectoryIds,
    maxFrame: trajectories.maxFrame,
  };
}

export default connect(mapStateToProps, actions)(Menu);
