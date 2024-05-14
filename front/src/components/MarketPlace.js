import React, { useState, useEffect } from "react";
import {
  Space,
  Table,
  Button,
  FloatButton,
  Tooltip,
  Modal,
  Typography,
} from "antd";
import {
  DeleteOutlined,
  SyncOutlined,
  PlusCircleOutlined,
  EditOutlined,
} from "@ant-design/icons";
import TaskModal from "./TaskModal";
import axios from "axios";

const MarketPlace = () => {
    const [selectedTask, setSelectedTask] = useState(null);

    const [data, setData] = useState([]);
  const components = [
    ...new Set(data.flatMap((item) => item.registered_components)),
  ];

  const fetchData = () => {
    axios
      .get("http://127.0.0.1:5001/tasks")
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  };
  useEffect(fetchData, []);

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
      sorter: (a, b) => a.name.localeCompare(b.name),
      render: (name) => name,
    },
    {
      title: "CBR",
      dataIndex: "cbr",
      key: "cbr",
      render: (cbr) => (
        <Typography.Paragraph copyable>
          {/* <pre>{JSON.stringify(cbr, null, 2)}</pre> */}
          {JSON.stringify(cbr, null, 2)}
        </Typography.Paragraph>
      ),
    },
    {
      title: "Registered Components",
      dataIndex: "registered_components",
      key: "registered_components",
      filters: components.map((component) => ({
        text: component,
        value: component,
      })),
      onFilter: (value, record) => record.registered_components.includes(value),
      render: (registered_components) => (
        <Typography.Paragraph copyable>
          {/* <pre>{JSON.stringify(cbr, null, 2)}</pre> */}
          {JSON.stringify(registered_components, null, 2)}
        </Typography.Paragraph>
      ),
    },
    {
      title: "Action",
      key: "action",
      render: (_, record) => (
        <Space size="middle">
          <Button onClick={() => showTaskModal("update", record)}>
            <EditOutlined />
          </Button>
          <Button onClick={() => deleteRow(record.id)}>
            <DeleteOutlined />
          </Button>
        </Space>
      ),
    },
  ];

  function deleteRow(key) {
    console.log("Deleting row:", key);
    axios
      .delete(`http://127.0.0.1:5001/tasks/${key}`)
      .then(() => {
        fetchData();
      })
      .catch((error) => {
        console.error("Error deleting data:", error);
      });
  }

  const [taskModal, setTaskModal] = useState({
    isOpen: false,
    type: null,
  });

  const showTaskModal = (type, task) => {
    setTaskModal({ isOpen: true, type });
    if (type === 'add') {
        setSelectedTask(null);
    } else {
        setSelectedTask(task);
    }    
  };

  const handleTaskModalOk = () => {
    setTaskModal({ ...taskModal, isOpen: false });
  };

  const handleTaskModalCancel = () => {
    setTaskModal({ ...taskModal, isOpen: false });
  };

  return (
    <>
      <FloatButton.Group
        shape="circle"
        style={{
          right: 24,
        }}
      >
        <Tooltip title="Add New Task" placement="left">
          <FloatButton
            type="primary"
            icon={<PlusCircleOutlined />}
            onClick={() => showTaskModal("add")}
          />
        </Tooltip>

        <Tooltip title="Refresh data" placement="left">
          <FloatButton
            type="primary"
            icon={<SyncOutlined />}
            onClick={fetchData}
          />
        </Tooltip>
      </FloatButton.Group>
      <Modal
        title={
          taskModal.type === "add"
            ? "Add New Task"
            : "Update Task"
        }
        open={taskModal.isOpen}
        onOk={handleTaskModalOk}
        onCancel={handleTaskModalCancel}
      >
        <TaskModal task={selectedTask} tasks={data}/>
      </Modal>
      <Table
        columns={columns}
        dataSource={data}
        pagination={{ position: ["bottomLeft"] }}
      />
    </>
  );
};

export default MarketPlace;
