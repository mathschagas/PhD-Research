import React, { useState, useEffect } from "react";
import { Form, Input, Button } from "antd";
import axios from "axios";
const { TextArea } = Input;

const TaskModal = ({ task, tasks }) => {
  const [id, setId] = useState("");
  const [name, setName] = useState("");
  const [cbrAttr, setCbrAttr] = useState("");
  const [registeredComponents, setRegisteredComponents] = useState("");
  const [isButtonDisabled, setIsButtonDisabled] = useState(true);

  useEffect(() => {
    if (task) {
      setId(task.id);
      setName(task.name);
      setCbrAttr(JSON.stringify(task.cbr));
      setRegisteredComponents(JSON.stringify(task.registered_components));
    } else {
      setId("");
      setName("");
      setCbrAttr("");
      setRegisteredComponents("");
    }
  }, [task]);

  useEffect(() => {
    try {
      JSON.parse(cbrAttr);
      JSON.parse(registeredComponents);
      const isIdUsed = tasks.some(
        (t) => t.id === id && (!task || task.id !== id)
      );
      setIsButtonDisabled(
        !id || !name || !cbrAttr || !registeredComponents || isIdUsed
      );
    } catch {
      setIsButtonDisabled(true);
    }
  }, [id, name, cbrAttr, registeredComponents, task, tasks]);

  const isIdUsed = tasks.some((t) => t.id === id && (!task || task.id !== id));

  const handleSubmit = async (values) => {
    const inputData = {
      id: id,
      name: name,
      cbr: JSON.parse(cbrAttr),
      registered_components: JSON.parse(registeredComponents),
    };
    try {
      const response = await axios.post(
        `http://127.0.0.1:5001/tasks`,
        inputData
      );
      console.log(response.data);
    } catch (error) {
      console.log(inputData);
      console.error("There was an error!", error);
    }
  };

  return (
    <Form
      onFinish={handleSubmit}
      style={{
        margin: "auto",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <Form.Item
        label="ID"
        name="id"
        validateStatus={isIdUsed ? "error" : ""}
        help={isIdUsed ? "ID já está sendo usado" : ""}
      >
        <Input onChange={(e) => setId(e.target.value)} value={id} />
      </Form.Item>
      <Form.Item label="Name">
        <Input
          value={name}
          placeholder="Insert the name of the task."
          onChange={(e) => setName(e.target.value)}
        />
      </Form.Item>
      <Form.Item label="CBR">
        <TextArea
          rows={10}
          placeholder="Insert the CBR attributes with their respective weights"
          value={cbrAttr}
          onChange={(e) => setCbrAttr(e.target.value)}
        />
      </Form.Item>
      <Form.Item label="Registered Components">
        <TextArea
          rows={10}
          placeholder="Insert the registered components"
          value={registeredComponents}
          onChange={(e) => setRegisteredComponents(e.target.value)}
        />
      </Form.Item>
      <Form.Item style={{ textAlign: "center" }}>
        <Button
          type="primary"
          htmlType="submit"
          alignItems="center"
          disabled={isButtonDisabled}
        >
          Add Task
        </Button>
      </Form.Item>
    </Form>
  );
};

export default TaskModal;
