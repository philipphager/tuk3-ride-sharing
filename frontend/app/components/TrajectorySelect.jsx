import React from 'react';
import PropTypes from 'prop-types';
import { Select } from 'antd';

const TrajectorySelect = ({ options }) => {
  const compOptions = options.map(value => (
    <Select.Option value={value} key={value}>
      {value}
    </Select.Option>
  ));
  return (
    <Select
      showSearch
      style={{ width: 200 }}
      placeholder="Select a trajectory id"
    >
      {compOptions}
    </Select>
  );
};

TrajectorySelect.propTypes = {
  options: PropTypes.arrayOf(PropTypes.number).isRequired,
};

export default TrajectorySelect;
