import React, { useState, useEffect } from "react";
import {
  Space,
  Table,
  Tag,
  Button,
  FloatButton,
  Tooltip,
  Card,
  Spin,
  Modal,
  Checkbox,
  List,
} from "antd";
import { SyncOutlined, UnorderedListOutlined } from "@ant-design/icons";
import axios from "axios";

function GetSNInfo() {
  const [tasksList, setTasksList] = useState([]);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [selectedTasks, setSelectedTasks] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [data, setData] = useState([]);
  const [currentComponentPort, setCurrentComponentPort] = useState();

  const fetchData = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get(`${process.env.REACT_APP_SNMANAGER_URL}/get_data`);
      console.log("Data fetched successfully:", response.data);
      setData(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
      setData([]);
    }
    setIsLoading(false);
  };

  useEffect(() => {
    fetchData();
  }, []); // Add dependencies if any

  const showModal = (record) => {
    setCurrentComponentPort(record.port);
    axios
      .get(`http://127.0.0.1:${record.port}/info`)
      .then((response) => {
        const taskIds = response.data.component.registered_tasks.map(
          (task) => task.id
        );
        setSelectedTasks(taskIds);
      })
      .catch((error) => {
        console.error("Error fetching tasks:", error);
      });
    setIsModalVisible(true);
  };

  const handleOk = () => {
    let selectedTasksList = selectedTasks?.map((taskId) =>
      tasksList.find((task) => task.id === taskId)
    );
    axios
      .post(
        `http://127.0.0.1:${currentComponentPort}/register_tasks`,
        selectedTasksList
      )
      .then((response) => {
        console.log("Tasks registered successfully:", response.data);
      })
      .catch((error) => {
        console.error("Error registering tasks:", error);
      });
    setSelectedTasks([]);
    setCurrentComponentPort();
    setIsModalVisible(false);
    fetchData();
  };

  const handleCancel = () => {
    setSelectedTasks([]);
    setCurrentComponentPort();
    setIsModalVisible(false);
  };

  const onChange = (checkedValues) => {
    setSelectedTasks(checkedValues);
  };

  const fetchTasks = async () => {
    try {
      const response = await axios.get(`${process.env.REACT_APP_MARKETPLACE_URL}/tasks`);
      setTasksList(
        response.data.map((task) => ({ id: task.id, name: task.name }))
      );
    } catch (error) {
      console.error("Error fetching tasks:", error);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const columns = [
    {
      align: "center",
      width: "5px",
      title: "ID",
      dataIndex: "id",
      key: "id",
      render: (id) => id,
    },
    {
      align: "center",
      width: "10px",
      title: "Type",
      dataIndex: "type",
      key: "type",
      render: (type) => String(type).toUpperCase(),
    },
    {
      align: "center",
      width: "10px",
      title: "Availability",
      key: "availability",
      dataIndex: "availability",
      render: (availability, record) => (
        <div style={{ display: "inline-block" }}>
          <Space size="small" direction="vertical">
            <Tag
              color={
                record.registered_tasks && record.registered_tasks.length > 0
                  ? "cyan"
                  : "warning"
              }
            >
              {record.registered_tasks && record.registered_tasks.length > 0
                ? "REGISTERED"
                : "UNREGISTERED"}
            </Tag>
            <Tag
              color={
                availability === "available"
                  ? "green"
                  : availability === "unavailable"
                  ? "volcano"
                  : "default"
              }
              key={availability}
            >
              {availability.toUpperCase()}
            </Tag>
          </Space>
        </div>
      ),
    },
    {
      align: "center",
      title: "Tasks",
      dataIndex: "registered_tasks",
      key: "tasks",
      render: (tasks) => {
        const removeDescription = (obj) => {
          if (Array.isArray(obj)) {
            return obj.map(removeDescription);
          } else if (typeof obj === "object" && obj !== null) {
            const { description, ...rest } = obj;
            return Object.fromEntries(
              Object.entries(rest).map(([key, value]) => [
                key,
                removeDescription(value),
              ])
            );
          }
          return obj;
        };

        const tasksWithoutDescription = tasks.map(removeDescription);

        return (
          <Card align="left" style={{ overflow: "auto", maxHeight: "100px" }}>
            <List
              itemLayout="horizontal"
              dataSource={tasksWithoutDescription}
              renderItem={(task, index) => (
                <List.Item key={index}>
                  <List.Item.Meta
                    title={<Tag color="blue">{task.name}</Tag>}
                  />
                </List.Item>
              )}
            />
          </Card>
        );
      },
    },
    {
      align: "center",
      width: "10px",
      title: "Action",
      key: "action",
      render: (_, record) => (
        <Space size="middle">
          <Button onClick={() => showModal(record)}>
            <UnorderedListOutlined />
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <>
      <FloatButton.Group
        shape="circle"
        style={{
          right: 24,
        }}
      >
        {isLoading ? (
          <Spin />
        ) : (
          <Tooltip title="Refresh data" placement="left">
            <FloatButton
              type="primary"
              icon={<SyncOutlined />}
              onClick={fetchData}
            />
          </Tooltip>
        )}
      </FloatButton.Group>
      <Table
        columns={columns}
        dataSource={data}
        pagination={{ position: ["bottomLeft"] }}
      />
      <Modal
        title="Select Tasks"
        visible={isModalVisible}
        onOk={handleOk}
        onCancel={handleCancel}
      >
        <Space>
          <Checkbox.Group
            style={{ width: "100%", display: "flex", flexDirection: "column" }}
            onChange={onChange}
            value={selectedTasks} // Garante que este estado contém os IDs corretos das tarefas
          >
            {tasksList?.map((task) => (
              <Checkbox key={task.id} value={task.id}>
                {task.name}
              </Checkbox>
            ))}
          </Checkbox.Group>
        </Space>
      </Modal>
    </>
  );
}

export default GetSNInfo;
