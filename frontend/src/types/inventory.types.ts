export interface InventoryItem {
  id: string;
  name: string;
  price: number;
  category: string;
}

export interface Inventory {
  items: InventoryItem[];
  total_price: number;
}
