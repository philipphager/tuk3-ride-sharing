import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { Row, Col, Slider, Spin, Button, Modal, Select } from 'antd';
import formats from '../constants';
import * as actions from '../actions/trajectoryActions';
import TrajectorySelect from '../components/TrajectorySelect';
import getTimeStringFromFID from '../utils/trajectoryFrame';
import TimeChart from './TimeChart';

class Menu extends Component {
  static propTypes = {
    getTrajectories: PropTypes.func.isRequired,
    getTrajectory: PropTypes.func.isRequired,
    removeTrajectory: PropTypes.func.isRequired,
    changeMaxTrajectoryFrame: PropTypes.func.isRequired,
    trajectoryIds: PropTypes.arrayOf(PropTypes.number),
    maxFrame: PropTypes.number,
    // eslint-disable-next-line
    times: PropTypes.any,
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
      timeModalVisible: false,
      format: formats[0].value,
    };
  }

  componentWillMount() {
    this.props.getTrajectories(this.state.format);
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

  onTimeButtonClick = () => {
    this.setState({ timeModalVisible: true });
  }

  onTimeModalCloseClick = () => {
    this.setState({ timeModalVisible: false });
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
    return getTimeStringFromFID(value);
  }

  handlePlay = () => {
    this.setState({ isPlaying: !this.state.isPlaying });
  }

  handleFormatSelect = (value) => {
    this.setState({ format: value });
    this.props.getTrajectories(this.state.format);
  }

  render() {
    const marks = {
      0: '0',
      1440: '12',
      2880: '24',
    };

    const frameOptions = formats.map(obj => (
      <Select.Option value={obj.value}>{obj.name}</Select.Option>
    ));
    return (
      <div className="menu">
        <Row>
          <Col span={3}>
            <Row>
              <span className="menuInfo">Format</span>
            </Row>
            <Row>
              <Select
                style={{ width: '100%' }}
                value={this.state.format}
                onSelect={this.handleFormatSelect}
              >
                {frameOptions}
              </Select>
            </Row>
          </Col>
          <Col span={3}>
            <Row>
              <span className="menuInfo">Trajectory Id:</span>
            </Row>
            <Row>
              {this.props.trajectoryIds ? (
                <TrajectorySelect
                  options={this.props.trajectoryIds.slice(0, 100)}
                  onSelect={value => this.props.getTrajectory(value, this.state.format)}
                  onDeselect={this.props.removeTrajectory}
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
                marks={marks}
                max={2880}
                onChange={this.handleTimeChange}
                tipFormatter={this.handleFormat}
              />
            </Row>
          </Col>
          <Col>
            <Button
              onClick={this.onTimeButtonClick}
            >
            Show Times
            </Button>
          </Col>
        </Row>
        <Modal
          title="Time Overview"
          visible={this.state.timeModalVisible}
          onOk={this.onTimeModalCloseClick}
          okText="Close"
          okCancel={false}
        >
          <TimeChart times={this.props.times} />
        </Modal>
      </div>
    );
  }
}

function mapStateToProps({ trajectories, time }) {
  return {
    trajectoryIds: trajectories.trejectoryIds,
    maxFrame: trajectories.maxFrame,
    times: time.times,
  };
}

export default connect(mapStateToProps, actions)(Menu);
