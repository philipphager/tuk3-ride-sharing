import React from 'react';
import PropTypes from 'prop-types';
import { Select } from 'antd';

const TrajectorySelect = ({ options, onChange }) => {
  const compOptions = options.map(value => (
    <Select.Option value={value} key={value}>
      {value}
    </Select.Option>
  ));
  return (
    <Select
      showSearch
      style={{ width: 100 }}
      placeholder="TrajectoryId"
      onChange={onChange}
    >
      {compOptions}
    </Select>
  );
};

TrajectorySelect.propTypes = {
  options: PropTypes.arrayOf(PropTypes.number).isRequired,
  onChange: PropTypes.func.isRequired,
};

export default TrajectorySelect;
