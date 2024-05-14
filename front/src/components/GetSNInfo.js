import React, { useState } from "react";
import { Space, Table, Tag, Button, FloatButton, Tooltip, Modal, Typography } from "antd";
import {
  DeleteOutlined,
  SyncOutlined,
  PlusCircleOutlined,
  EditOutlined,
} from "@ant-design/icons";
import AddComponentForm from "./ComponentModal";

function GetSNInfo() {
  const columns = [
    {
      title: "ID",
      dataIndex: "id",
      key: "id",
      render: (id) => id,
    },
    {
      title: "CBR",
      dataIndex: "cbr",
      key: "cbr",
      render: cbr => (
        <Typography.Paragraph copyable>
          {/* <pre>{JSON.stringify(cbr, null, 2)}</pre> */}
          {JSON.stringify(cbr, null, 2)}
        </Typography.Paragraph>
      )
    },
    {
      title: "Status",
      key: "status",
      dataIndex: "status",
      render: (status) => (
              <Tag color={status === "available" ? "green" : "volcano"} key={status}>
                {status.toUpperCase()}
              </Tag>
            ),
    },
    {
      title: "Action",
      key: "action",
      render: (_, record) => (
        <Space size="middle">
          <Button onClick={() => showComponentModal('update')}>
            <EditOutlined />
          </Button>
          <Button>
            <SyncOutlined />
          </Button>
          <Button onClick={() => deleteRow(record.key)}>
            <DeleteOutlined />
          </Button>
        </Space>
      ),
    },
  ];
  const example_data = [
    {
      key: "1",
      id: "A",
      cbr: JSON.parse('{"name":"John", "age":30, "city":"New York"}'),
      status: "available",
    },
    {
      key: "2",
      id: "B",
      cbr: JSON.parse('{"name":"John", "age":30, "city":"New York"}'),
      status: "unavailable",
    },
    {
      key: "3",
      id: "C",
      cbr: JSON.parse('{"name":"John", "age":30, "city":"New York"}'),
      status: "available",
    },
  ];

  const [data, setData] = useState(example_data);
  const [componentModal, setComponentModal] = useState({ isOpen: false, type: null });

  const showComponentModal = (type) => {
    setComponentModal({ isOpen: true, type });
  }

  const handleComponentModalOk = () => {
    setComponentModal({ ...componentModal, isOpen: false });
  }

  const handleComponentModalCancel = () => {
    setComponentModal({ ...componentModal, isOpen: false });
  }

  // Function to delete a row
  function deleteRow(key) {
    setData(data.filter((item) => item.key !== key));
  }

  return (
    <>
      <FloatButton.Group
        shape="circle"
        style={{
          right: 24,
        }}
      >
        <Tooltip title="Add New Component" placement="left">
          <FloatButton
            type="primary"
            icon={<PlusCircleOutlined />}
            onClick={() => showComponentModal('add')}
          />
        </Tooltip>

        <Tooltip title="Refresh data" placement="left">
          <FloatButton type="primary" icon={<SyncOutlined />} />
        </Tooltip>
      </FloatButton.Group>
      <Modal title={componentModal.type === "add" ? "Add New Component" : "Update Component"} open={componentModal.isOpen} onOk={handleComponentModalOk} onCancel={handleComponentModalCancel}>
        <AddComponentForm />
      </Modal>
      <Table
        columns={columns}
        dataSource={data}
        pagination={{ position: ["bottomLeft"] }}
      />
    </>
  );
}

export default GetSNInfo;
