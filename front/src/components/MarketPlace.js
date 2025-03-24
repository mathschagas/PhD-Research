import React, { useState, useEffect } from "react";
import { Space, Table, Button, FloatButton, Tooltip } from "antd";
import {
  DeleteOutlined,
  SyncOutlined,
  PlusCircleOutlined,
  EditOutlined,
} from "@ant-design/icons";
import axios from "axios";
import TaskDetails from "./TaskDetails";
import { useNavigate } from "react-router-dom";

// MarketPlace Component
const MarketPlace = () => {
  // State for the selected task and tasks data from API
  const [tasksData, setTasksData] = useState([]);
  const navigate = useNavigate();

  // Function to fetch data from the API
  const fetchData = () => {
    axios
      .get(`${process.env.MARKETPLACE_URL}/tasks`)
      .then((response) => {
        setTasksData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  };

  // Fetch data on component mount
  useEffect(fetchData, []);

  // Table columns configuration
  const columns = [
    {
      title: "ID",
      dataIndex: "id",
      key: "id",
      defaultSortOrder: "ascend",
      sorter: (a, b) => a.id - b.id,
      render: (id) => id,
    },
    {
      title: "Task Name",
      dataIndex: "name",
      key: "name",
      defaultSortOrder: "ascend",
      sorter: (a, b) => {
        if (!a.name && !b.name) return 0;
        if (!a.name) return -1;
        if (!b.name) return 1;
        return a.name.localeCompare(b.name);
      },
      render: (name) => name,
    },
    {
      title: "Description",
      dataIndex: "description",
      key: "description",
      defaultSortOrder: "ascend",
      sorter: (a, b) => {
        if (!a.description && !b.description) return 0;
        if (!a.description) return -1;
        if (!b.description) return 1;
        return a.description.localeCompare(b.description);
      },
      render: (description) => description,
    },
    {
      title: "Action",
      key: "action",
      render: (_, record) => (
        <Space size="middle">
          <Button onClick={() => navigate(`/marketplace/edit_task/${record.id}`)}>
            <EditOutlined />
          </Button>
          <Button onClick={() => deleteRow(record.id)}>
            <DeleteOutlined />
          </Button>
        </Space>
      ),
    },
  ];

  // Function to delete a row from the table
  function deleteRow(key) {
    console.log("Deleting row:", key);
    axios
      .delete(`${process.env.MARKETPLACE_URL}/tasks/${key}`)
      .then(() => {
        fetchData();
      })
      .catch((error) => {
        console.error("Error deleting data:", error);
      });
  }

  // Return the MarketPlace component
  return (
    <>
      {/* Floating action buttons */}
      <FloatButton.Group
        shape="circle"
        style={{
          right: 24,
        }}
      >
        {/* Add new task button */}
        <Tooltip title="Add New Task" placement="left">
          <FloatButton
            type="primary"
            icon={<PlusCircleOutlined />}
            onClick={() => navigate("/marketplace/new_task")}
          />
        </Tooltip>

        {/* Refresh data button */}
        <Tooltip title="Refresh data" placement="left">
          <FloatButton
            type="primary"
            icon={<SyncOutlined />}
            onClick={fetchData}
          />
        </Tooltip>
      </FloatButton.Group>

      {/* Table component */}
      <Table
        columns={columns}
        rowKey={(record) => record.id}
        expandable={{
          expandedRowRender: (record) => <TaskDetails task={record} />,
          rowExpandable: (record) => {
            return record.name !== "Not Expandable";
          },
        }}
        dataSource={tasksData}
        pagination={{ position: ["bottomLeft"] }}
      />

    </>
  );
};

export default MarketPlace;
