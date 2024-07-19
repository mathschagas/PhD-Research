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
} from "antd";
import { SyncOutlined, UnorderedListOutlined } from "@ant-design/icons";
import axios from "axios";

function GetSNInfo() {
  const columns = [
    {
      align: "center",
      width: "5px",
      title: "ID",
      dataIndex: "port",
      key: "id",
      render: (port) => port,
    },
    {
      align: "center",
      width: "10px",
      title: "Name",
      dataIndex: "name",
      key: "name",
      render: (name) => name,
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
            <pre>{JSON.stringify(tasksWithoutDescription, null, 2)}</pre>
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
          <Button>
            <UnorderedListOutlined />
          </Button>
        </Space>
      ),
    },
  ];

  const [isLoading, setIsLoading] = useState(false);
  const [data, setData] = useState([]);

  const fetchData = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get("http://127.0.0.1:5001/get_data");
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
    </>
  );
}

export default GetSNInfo;
