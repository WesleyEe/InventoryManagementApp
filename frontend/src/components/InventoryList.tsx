import React from "react";
import { Table } from "antd";
import { Inventory } from "@appTypes/inventory.types";

interface InventoryListProps {
  data: Inventory;
  loading: boolean;
}

const InventoryList: React.FC<InventoryListProps> = ({ data, loading }) => {
  const columns = [
    {
      title: "Name",
      dataIndex: "name",
      key: "name",
    },
    {
      title: "Price",
      dataIndex: "price",
      key: "price",
      render: (price: number) => `$${price}`,
    },
    {
      title: "Category",
      dataIndex: "category",
      key: "category",
    },
  ];

  return (
    <>
      <Table
        columns={columns}
        dataSource={data.items}
        loading={loading}
        rowKey="id"
        bordered
        footer={() => (
          <div
            style={{
              textAlign: "right",
              fontSize: "16px",
              fontWeight: "bold",
              color: "#666",
            }}
          >
            Total Price: ${data.total_price}
          </div>
        )}
      />
    </>
  );
};

export default InventoryList;
