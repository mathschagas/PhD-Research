import React, { useState, useEffect } from "react";
import axios from "axios";
import { Select, Typography, Layout, Button, Table, Descriptions } from "antd";

const { Title } = Typography;
const { Option } = Select;
const { Content } = Layout;

const Delegation = () => {
  const [delegationData, setDelegationData] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [selectedTask, setSelectedTask] = useState(undefined);
  const [selectedScenario, setSelectedScenario] = useState(undefined);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/tasks");
        setTasks(response.data);
      } catch (error) {
        console.error("Error fetching tasks:", error);
      }
    };
    fetchTasks();
  }, []);

  const fetchDelegationData = async () => {
    if (selectedTask && selectedScenario) {
      setLoading(true);
      try {
        const response = await axios.get(
          `http://127.0.0.1:5001/request_delegation/${selectedTask}/${encodeURIComponent(
            selectedScenario
          )}`
        );
        setDelegationData(response.data);
      } catch (error) {
        console.error("Error fetching data:", error);
        setDelegationData(null);
      } finally {
        setLoading(false);
      }
    }
  };

  // Função auxiliar para determinar se um objeto é simples (não um array e não aninhado)
  const isSimpleObject = (obj) => {
    return (
      obj &&
      typeof obj === "object" &&
      !Array.isArray(obj) &&
      Object.values(obj).every((value) => typeof value !== "object")
    );
  };

  // Componente para renderizar um objeto simples com `Descriptions`
  const RenderSimpleObject = ({ data }) => (
    <Descriptions bordered column={1}>
      {Object.entries(data).map(([key, value]) => (
        <Descriptions.Item label={key} key={key}>
          {value.toString()}
        </Descriptions.Item>
      ))}
    </Descriptions>
  );

  // Componente para renderizar uma lista de objetos com `Table`
  const RenderObjectList = ({ data }) => {
    const columns = Object.keys(data[0]).map((key) => ({
      title: key,
      dataIndex: key,
      key: key,
    }));

    return (
      <Table
        dataSource={data}
        columns={columns}
        rowKey="id"
        pagination={false}
      />
    );
  };

  // Componente para decidir qual renderizador usar baseado nos dados
  const RenderJSON = ({ data }) => {
    if (Array.isArray(data) && data.length > 0 && isSimpleObject(data[0])) {
      return <RenderObjectList data={data} />;
    } else if (isSimpleObject(data)) {
      return <RenderSimpleObject data={data} />;
    } else {
      // Fallback para dados não suportados ou complexos
      return <pre>{JSON.stringify(data, null, 2)}</pre>;
    }
  };

  return (
    <Layout>
      <Content style={{ padding: "50px", maxWidth: "600px", margin: "0 auto" }}>
        <Title level={2} style={{ textAlign: "center" }}>
          Delegation
        </Title>
        <Select
          showSearch
          style={{ width: "100%", marginBottom: "20px" }}
          placeholder="Select a Task"
          optionFilterProp="children"
          onChange={setSelectedTask}
          filterOption={(input, option) =>
            option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
          }
        >
          {tasks.map((task) => (
            <Option key={task.id} value={task.id}>
              {task.name}
            </Option>
          ))}
        </Select>
        {selectedTask && (
          <Select
            showSearch
            style={{ width: "100%", marginBottom: "20px" }}
            placeholder="Select a Scenario"
            optionFilterProp="children"
            onChange={(value) => setSelectedScenario(value)}
            filterOption={(input, option) =>
              option.children.toLowerCase().indexOf(input.toLowerCase()) >= 0
            }
          >
            {tasks
              .find((task) => task.id === selectedTask)
              ?.scenarios.map((scenario, index) => (
                <Option key={scenario.name} value={scenario.name}>
                  {scenario.name}
                </Option>
              ))}
          </Select>
        )}
        <Button
          type="primary"
          loading={loading}
          onClick={fetchDelegationData}
          disabled={!selectedTask || !selectedScenario}
          style={{ marginBottom: "20px" }}
        >
          Fetch Delegation Data
        </Button>
        <RenderJSON data={delegationData} />
      </Content>
    </Layout>
  );
};

export default Delegation;
