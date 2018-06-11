import React, { Component, Fragment } from 'react';
import PropTypes from 'prop-types';
import { XYPlot, VerticalGridLines, HorizontalGridLines, XAxis, YAxis, VerticalBarSeries, DiscreteColorLegend } from 'react-vis';
import randomMC from 'random-material-color';

class TimeChart extends Component {
  componentWillMount = () => {

  }

  render() {
    const formats = Object.keys(this.props.times);
    const actions = Object.keys(this.props.times[formats[0]]);
    const bars = [];
    const legendItems = [];
    formats.forEach((format) => {
      const data = [];
      actions.forEach((action) => {
        let total = 0;
        const values = this.props.times[format][action];
        values.forEach((value) => {
          total += value;
        });
        let avg = 0;
        if (values.length > 0) {
          avg = total / values.length;
        }
        data.push({ x: action, y: avg });
      });
      const newColor = randomMC.getColor();
      legendItems.push({ title: format, color: newColor });
      bars.push(<VerticalBarSeries
        cluster={format}
        color={newColor}
        data={data}
        key={format}
      />);
    });
    return (
      <Fragment>
        <DiscreteColorLegend
          orientation="horizontal"
          width={500}
          style={{ height: '30px' }}
          colors={legendItems.map(value => value.color)}
          items={legendItems.map(value => value.title)}
        />
        <XYPlot
          width={500}
          height={500}
          xType="ordinal"
          stackBy="y"
        >
          <VerticalGridLines />
          <HorizontalGridLines />
          <XAxis />
          <YAxis />
          {bars}
        </XYPlot>
      </Fragment>
    );
  }
}

TimeChart.propTypes = {
  // eslint-disable-next-line
  times: PropTypes.any,
};

export default TimeChart;
