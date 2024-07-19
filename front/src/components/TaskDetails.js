import React from "react";
import { Descriptions } from "antd";

const TaskDetails = ({ task }) => {
  const taskCopy = { ...task };
  delete taskCopy.id;
  delete taskCopy.name;
  delete taskCopy.description;

  const items = Object.keys(taskCopy).map((key) => {
    let value = task[key];
    if (typeof value === "object" && value !== null) {
      value = JSON.stringify(value, null, 2);
    }
    return {
      key: key,
      label: key,
      children: value,
    };
  });

  return <Descriptions bordered size="small" layout="vertical" items={items} />;
};

export default TaskDetails;
