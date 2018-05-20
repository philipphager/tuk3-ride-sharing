import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Dimensions from 'react-dimensions';
import ReactMapGL from 'react-map-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import { connect } from 'react-redux';
import { Spin } from 'antd';
import * as actions from '../actions/mapActions';
import DeckGlLayer from '../components/DeckGLLayer';

const ResizableMap = Dimensions({
  elementResize: true,
})(class Map extends Component {
  static propTypes = {
    containerWidth: PropTypes.number.isRequired,
    containerHeight: PropTypes.number.isRequired,
    viewport: PropTypes.shape({
      height: PropTypes.number,
      width: PropTypes.number,
      latitude: PropTypes.number,
      longitude: PropTypes.number,
      zoom: PropTypes.number,
    }).isRequired,
    // eslint-disable-next-line
    data: PropTypes.array,
    changeViewport: PropTypes.func.isRequired,
    changeContainerSize: PropTypes.func.isRequired,
    isFetching: PropTypes.bool,
    maxFrame: PropTypes.number,
  };

  static defaultProps = {
    data: null,
    maxFrame: 2880,
    isFetching: false,
  }

  componentWillMount() {
    this.props.changeContainerSize(this.props.containerWidth, this.props.containerHeight);
  }

  handleViewportChange = (viewport) => {
    this.props.changeViewport(viewport);
  }

  render() {
    const trajectoriesData = this.props.data.map(trajectoryData => (
      {
        type: trajectoryData.geoJsonData.type,
        properties: {
          color: [255, 0, 0, 255],
          ...trajectoryData.geoJsonData.properties,
        },
        geometry: {
          // eslint-disable-next-line
          coordinates: trajectoryData.geoJsonData.geometry.coordinates.slice(0, this.props.maxFrame),
          type: trajectoryData.geoJsonData.geometry.type,
        },
      }
    ));
    return (
      <Spin tip="Loading Trajectory..." spinning={this.props.isFetching}>
        <ReactMapGL
          {...this.props.viewport}
          onViewportChange={viewport => this.handleViewportChange(viewport)}
        >
          {this.props.data.length > 0 ?
            <DeckGlLayer
              data={trajectoriesData}
              viewport={this.props.viewport}
            />
            : null}
        </ReactMapGL>
      </Spin>
    );
  }
});

function mapStateToProps({ map, trajectories }) {
  return {
    viewport: map.viewport,
    data: trajectories.trajectoriesData,
    isFetching: trajectories.isFetching,
    maxFrame: trajectories.maxFrame,
  };
}

export default connect(mapStateToProps, actions)(ResizableMap);
