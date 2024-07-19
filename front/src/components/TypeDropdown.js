import React from 'react';
import { Select } from 'antd';

const { Option } = Select;

const TypeDropdown = ({ value, onChange }) => {
  const handleChange = (selectedValue) => {
	onChange(selectedValue);
  };

  return (
	<Select value={value} onChange={handleChange} placeholder="Select a type" style={{ width: 120 }}>
	  <Option value="int">Integer</Option>
	  <Option value="str">String</Option>
	  <Option value="bool">Boolean</Option>
	</Select>
  );
};

export default TypeDropdown;