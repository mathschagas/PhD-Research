import React, { useState, useEffect } from "react";
import TypeDropdown from "./TypeDropdown";
import { Form, Input, Button, Space, Select, Card } from "antd";
import { MinusCircleOutlined, PlusOutlined } from "@ant-design/icons";
import axios from "axios";
import { useNavigate, useParams } from "react-router-dom";

const EditTaskPage = () => {
  const { taskId } = useParams();
  const [form] = Form.useForm();
  const isUpdating = taskId !== undefined;
  const [allTasksData, setAllTasksData] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    axios
      .get(`${process.env.REACT_APP_MARKETPLACE_URL}/tasks`)
      .then((response) => {
        setAllTasksData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching task IDs:", error);
      });
  }, []);

  useEffect(() => {
    if (isUpdating) {
      console.log("Fetching Task with ID:", taskId);
      axios
        .get(`${process.env.REACT_APP_MARKETPLACE_URL}/tasks/${taskId}`)
        .then((response) => {
          form.setFieldsValue(response.data);
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    } else {
      form.setFieldsValue({
        scenarios: [{ name: "Default", constraints: [], cbr_attributes: [] }],
      });
    }
  }, [form, taskId, isUpdating]);

  const onFinish = async (values) => {
    console.log("Form values:", values);
    try {
      if (isUpdating) {

        console.log("Updating Task with ID:", taskId);
        const response = await axios.put(
          `${process.env.REACT_APP_MARKETPLACE_URL}/tasks/${taskId}`,
          values
        );
        console.log("Task updated successfully:", response.data);
      } else {
        console.log("Creating new Task");
        const response = await axios.post(
          `${process.env.REACT_APP_MARKETPLACE_URL}/tasks`,
          values
        );
        console.log("Task created successfully:", response.data);
      }
      navigate("/marketplace");
    } catch (error) {
      console.error(
        "Error in API call:",
        error.response ? error.response.data : error.message
      );
    }
  };

  const checkIdExists = async (id) => {
    return allTasksData.some((task) => (String(task.id) === String(id)));
  };

  return (
    <Form name="editTask" form={form} onFinish={onFinish} layout="vertical">
      {/* Task ID */}
      <Form.Item
        label="ID"
        name="id"
        rules={[
          {
            required: true,
            message: "Please enter the task ID!",
          },
          () => ({
            validator(_, value) {
              if (isUpdating && String(taskId) === String(value)) {
                console.log("Same ID as before:", value);
                return Promise.resolve();
              }
              return checkIdExists(value).then((result) => {
                if (result) {
                  return Promise.reject(new Error("Task ID already exists!"));
                }
                return Promise.resolve();
              });
            },
          }),
        ]}
      >
        <Input disabled={isUpdating} />
      </Form.Item>

      {/* Task Name */}
      <Form.Item
        label="Name"
        name="name"
        rules={[
          {
            required: true,
            message: "Please enter the task name!",
          },
        ]}
      >
        <Input />
      </Form.Item>

      {/* Task Description */}
      <Form.Item label="Description" name="description">
        <Input.TextArea />
      </Form.Item>

      {/* Context Descriptors */}
      <Form.Item label="Context Descriptors">
        <Form.List name="context_descriptors">
          {(fields, { add, remove }) => (
            <>
              {/* For each context descriptor */}
              {fields.map(({ key, name, ...restField }) => (
                <Space key={key} style={{ display: "flex" }} align="baseline">
                  {/* Context Descriptor Name */}
                  <Form.Item
                    {...restField}
                    name={[name, "name"]}
                    rules={[
                      {
                        required: true,
                        message: "Missing descriptor name",
                      },
                    ]}
                    label="Name"
                  >
                    <Input placeholder="Descriptor Name" />
                  </Form.Item>

                  {/* Context Descriptor Type (TODO: check if this is really necessary */}
                  <Form.Item
                    {...restField} // Use restField for consistent field properties
                    name={[name, "type"]} // Corrected to use dynamic name for unique path
                    rules={[
                      {
                        required: true,
                        message: "Please select a descriptor type",
                      },
                    ]}
                    label="Type"
                  >
                    <TypeDropdown />
                  </Form.Item>

                  {/* Remove context descriptor button */}
                  <MinusCircleOutlined onClick={() => remove(name)} />
                </Space>
              ))}
              <Form.Item>
                <Button
                  type="dashed"
                  onClick={() => add()}
                  block
                  icon={<PlusOutlined />}
                >
                  Add Context Descriptor
                </Button>
              </Form.Item>
            </>
          )}
        </Form.List>
      </Form.Item>

      {/* Scenarios */}
      <Form.Item label="Scenarios">
        <Form.List name="scenarios">
          {(scenarioFields, { add: addScenario, remove: removeScenario }) => (
            <>
              {scenarioFields.map(({ key, name, ...restField }) => (
                <Card
                  style={{
                    marginBottom: 16,
                  }}
                  title={
                    key === 0 ? "Default Scenario" : `Extra Scenario ${key + 1}`
                  }
                  extra={
                    // Insert remove button only if it is an extra scenario
                    scenarioFields.length > 1 &&
                    form.getFieldValue("scenarios")[key]?.name !==
                      "Default" && (
                      <MinusCircleOutlined
                        onClick={() => removeScenario(name)}
                      />
                    )
                  }
                >
                  <Form.Item
                    {...restField}
                    name={[name, "name"]}
                    rules={[
                      {
                        required: true,
                        message: "Missing scenario name",
                      },
                    ]}
                    label="Scenario Name"
                  >
                    <Input placeholder="Scenario Name" disabled={key === 0} />
                  </Form.Item>

                  <Space
                    key={key}
                    style={{
                      display: "flex",
                      flexDirection: "column",
                      marginBottom: 8,
                    }}
                    align="baseline"
                  >
                    <Form.Item label="Contraints">
                      <Form.List name={[name, "constraints"]}>
                        {(
                          constraintFields,
                          { add: addConstraint, remove: removeConstraint }
                        ) => (
                          <>
                            {constraintFields?.map((constraintField) => (
                              <Space key={constraintField.key} align="baseline">
                                <Form.Item
                                  {...constraintField}
                                  name={[constraintField.name, "name"]}
                                  rules={[
                                    {
                                      required: true,
                                      message: "Missing constraint name",
                                    },
                                  ]}
                                >
                                  <Input placeholder="Attribute Name" />
                                </Form.Item>
                                <Form.Item
                                  {...constraintField}
                                  name={[constraintField.name, "operator"]}
                                  rules={[
                                    {
                                      required: true,
                                      message: "Missing operator",
                                    },
                                  ]}
                                >
                                  <Select placeholder="Operator">
                                    <Select.Option value="less">
                                      &lt;
                                    </Select.Option>
                                    <Select.Option value="greater">
                                      &gt;
                                    </Select.Option>
                                    <Select.Option value="equal">
                                      =
                                    </Select.Option>
                                    <Select.Option value="notEqual">
                                      &ne;
                                    </Select.Option>
                                    <Select.Option value="lessOrEqual">
                                      &le;
                                    </Select.Option>
                                    <Select.Option value="greaterOrEqual">
                                      &ge;
                                    </Select.Option>
                                  </Select>
                                </Form.Item>
                                <Form.Item
                                  {...constraintField}
                                  name={[constraintField.name, "value"]}
                                  rules={[
                                    {
                                      required: true,
                                      message: "Missing value",
                                    },
                                  ]}
                                >
                                  <Input placeholder="Value" type="number" />
                                </Form.Item>
                                <Form.Item
                                  {...constraintField}
                                  name={[constraintField.name, "weight"]}
                                  rules={[
                                    {
                                      required: true,
                                      message: "Missing weight",
                                    },
                                  ]}
                                >
                                  <Input
                                    placeholder="Default Weight"
                                    type="number"
                                  />
                                </Form.Item>
                                <MinusCircleOutlined
                                  onClick={() =>
                                    removeConstraint(constraintField.name)
                                  }
                                />
                              </Space>
                            ))}
                            <Button
                              type="dashed"
                              onClick={() => {
                                console.log("Adding Constraint");
                                addConstraint();
                              }}
                              block
                              icon={<PlusOutlined />}
                            >
                              Add Constraint
                            </Button>
                          </>
                        )}
                      </Form.List>
                    </Form.Item>

                    {/* cbr_attributes.max and cbr_attributes.min */}
                    <Form.Item label="Cost, Benefit & Risk Attributes">
                      <Form.List name={[name, "cbr_attributes"]}>
                        {(
                          cbrAttributesFields,
                          { add: addCBRAttribute, remove: removeCBRAttribute }
                        ) => (
                          <>
                            {cbrAttributesFields?.map((cbrAttributeField) => (
                              <Space
                                key={cbrAttributeField.key}
                                display="flex"
                                align="baseline"
                              >
                                <Form.Item
                                  {...cbrAttributeField}
                                  name={[cbrAttributeField.name, "type"]}
                                  rules={[
                                    {
                                      required: true,
                                      message:
                                        "Missing CBR Attribute objective",
                                    },
                                  ]}
                                >
                                  <Select>
                                    <Select.Option value="max">
                                      MAX
                                    </Select.Option>
                                    <Select.Option value="min">
                                      MIN
                                    </Select.Option>
                                  </Select>
                                </Form.Item>
                                <Form.Item
                                  {...cbrAttributeField}
                                  name={[cbrAttributeField.name, "name"]}
                                  fieldKey={[
                                    cbrAttributeField.fieldKey,
                                    "name",
                                  ]}
                                  rules={[
                                    {
                                      required: true,
                                      message: "Missing CBR Attribute name",
                                    },
                                  ]}
                                >
                                  <Input placeholder="CBR Attribute Name" />
                                </Form.Item>
                                <Form.Item
                                  {...cbrAttributeField}
                                  name={[cbrAttributeField.name, "weight"]}
                                  rules={[
                                    {
                                      required: true,
                                      message: "Missing weight",
                                    },
                                  ]}
                                >
                                  <Input
                                    placeholder="Default Weight"
                                    type="number"
                                  />
                                </Form.Item>
                                <MinusCircleOutlined
                                  onClick={() =>
                                    removeCBRAttribute(cbrAttributeField.name)
                                  }
                                />
                              </Space>
                            ))}
                            <Button
                              type="dashed"
                              onClick={() => {
                                console.log("Adding CBR Attribute");
                                addCBRAttribute();
                              }}
                              block
                              icon={<PlusOutlined />}
                            >
                              Add CBR Attribute
                            </Button>
                          </>
                        )}
                      </Form.List>
                    </Form.Item>
                  </Space>
                </Card>
              ))}
              <Button
                type="dashed"
                onClick={() => addScenario()}
                block
                icon={<PlusOutlined />}
              >
                Add Scenario
              </Button>
            </>
          )}
        </Form.List>
      </Form.Item>

      <Form.Item>
        <Button type="primary" htmlType="submit">
          {isUpdating ? "Update Task" : "Create Task"}
        </Button>
      </Form.Item>
    </Form>
  );
};

export default EditTaskPage;
