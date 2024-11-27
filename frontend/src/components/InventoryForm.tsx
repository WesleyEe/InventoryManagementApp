import React from "react";
import { Form, Input, InputNumber, Select, Button, message } from "antd";
import api from "@services/api";
import { InventoryItem } from "@appTypes/inventory.types";

interface InventoryFormProps {
  onItemAdded: () => void;
}

const { Option } = Select;

const InventoryForm: React.FC<InventoryFormProps> = ({ onItemAdded }) => {
  const [form] = Form.useForm();

  const onFinish = async (values: InventoryItem) => {
    try {
      await api.post("/item", values);
      message.success("Item added successfully!");
      form.resetFields();
      onItemAdded();
    } catch (error) {
      message.error("Failed to add item.");
    }
  };

  return (
    <Form
      form={form}
      layout="vertical"
      onFinish={onFinish}
      initialValues={{ category: "General" }}
    >
      <Form.Item
        label="Name"
        name="name"
        rules={[{ required: true, message: "Please enter the item name" }]}
      >
        <Input placeholder="Item name" />
      </Form.Item>

      <Form.Item
        label="Price"
        name="price"
        rules={[
          { required: true, message: "Please enter the price" },
          {
            type: "number",
            min: 0,
            message: "Price must be a positive number",
          },
        ]}
      >
        <InputNumber placeholder="Price" style={{ width: "100%" }} />
      </Form.Item>

      <Form.Item
        label="Category"
        name="category"
        rules={[{ required: true, message: "Please select a category" }]}
      >
        <Select>
          <Option value="General">General</Option>
          <Option value="Electronics">Electronics</Option>
          <Option value="Clothing">Clothing</Option>
          <Option value="Stationary">Stationary</Option>
          <Option value="Books">Books</Option>
        </Select>
      </Form.Item>

      <Form.Item>
        <Button type="primary" htmlType="submit">
          Add Item
        </Button>
      </Form.Item>
    </Form>
  );
};

export default InventoryForm;
