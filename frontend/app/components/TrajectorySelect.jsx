import React from 'react';
import PropTypes from 'prop-types';
import { Select } from 'antd';

const TrajectorySelect = ({ options, onSelect, onDeselect }) => {
  const compOptions = options.map(value => (
    <Select.Option value={value} key={value}>
      {value}
    </Select.Option>
  ));
  return (
    <Select
      mode="multiple"
      showSearch
      style={{ width: '100%' }}
      placeholder="Please select one TID"
      onSelect={onSelect}
      onDeselect={onDeselect}
    >
      {compOptions}
    </Select>
  );
};

TrajectorySelect.propTypes = {
  options: PropTypes.arrayOf(PropTypes.number).isRequired,
  onSelect: PropTypes.func.isRequired,
  onDeselect: PropTypes.func.isRequired,
};

export default TrajectorySelect;
