import React, { useState, useEffect } from "react";
import { message } from "antd";
import api from "@services/api";
import InventoryForm from "@components/InventoryForm";
import InventoryList from "@components/InventoryList";
import { Inventory } from "@appTypes/inventory.types";

const InventoryManager: React.FC = () => {
  const [inventory, setInventory] = useState<Inventory>({
    items: [],
    total_price: 0,
  });
  const [loading, setLoading] = useState<boolean>(true);

  const fetchInventory = async () => {
    try {
      const response = await api.get<Inventory>("/items");
      setInventory(response.data);
    } catch (error) {
      message.error("Failed to load inventory data.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchInventory();
  }, []);

  return (
    <>
      <InventoryForm onItemAdded={fetchInventory} />
      <InventoryList data={inventory} loading={loading} />
    </>
  );
};

export default InventoryManager;
