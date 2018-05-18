import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Dimensions from 'react-dimensions';
import ReactMapGL from 'react-map-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import { connect } from 'react-redux';
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
    data: PropTypes.func.isRequired,
    changeViewport: PropTypes.func.isRequired,
    changeContainerSize: PropTypes.func.isRequired,
  };

  componentWillMount() {
    this.props.changeContainerSize(this.props.containerWidth, this.props.containerHeight);
  }

  handleViewportChange = (viewport) => {
    this.props.changeViewport(viewport);
  }

  render() {
    return (
      <ReactMapGL
        {...this.props.viewport}
        onViewportChange={viewport => this.handleViewportChange(viewport)}
      >
        {this.props.data ?
          <DeckGlLayer data={this.props.data} viewport={this.props.viewport} /> : null}
      </ReactMapGL>
    );
  }
});

function mapStateToProps({ map, trajectories }) {
  return {
    viewport: map.viewport,
    data: trajectories.trajectoryData,
  };
}

export default connect(mapStateToProps, actions)(ResizableMap);
