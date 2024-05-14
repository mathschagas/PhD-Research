import React, { useState, useEffect } from "react";
import { Form, Input, Button } from "antd";
import axios from "axios";
const { TextArea } = Input;

function ComponentModal() {
  const [name, setName] = useState("");
  const [inputJSON, setInputJSON] = useState("");
  const [isButtonDisabled, setIsButtonDisabled] = useState(true);

  useEffect(() => {
    try {
      JSON.parse(inputJSON);
      setIsButtonDisabled(!name || !inputJSON);
    } catch {
      setIsButtonDisabled(true);
    }
  }, [name, inputJSON]);

  const handleSubmit = async (values) => {
    try {
      const inputData = {
        [name]: JSON.parse(inputJSON),
      };
      const response = await axios.put(
        "http://localhost:5000/update_data",
        inputData
      );
      console.log(response.data);
    } catch (error) {
      console.error("There was an error!", error);
    }
  };

  return (
    <Form
      onFinish={handleSubmit}
      className="create-component-form"
      style={{
        margin: "auto",
        display: "flex",
        flexDirection: "column",
      }}
    >
      <Form.Item label="Name">
        <Input
          value={name}
          placeholder="Insert the name of the component."
          onChange={(e) => setName(e.target.value)}
        />
      </Form.Item>
      <Form.Item label="JSON">
        <TextArea
          rows={10}
          placeholder="Insert the JSON data of the component"
          value={inputJSON}
          onChange={(e) => setInputJSON(e.target.value)}
        />
      </Form.Item>
      <Form.Item style={{ textAlign: "center" }}>
        <Button
          type="primary"
          htmlType="submit"
          alignItems="center"
          disabled={isButtonDisabled}
        >
          Add Component
        </Button>
      </Form.Item>
    </Form>
  );
}

export default ComponentModal;
