import React from "react";
import { Layout, Typography } from "antd";
import InventoryManager from "@components/InventoryManager";

const { Header, Content } = Layout;
const { Title } = Typography;

const App: React.FC = () => {
  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Header
        style={{
          background: "#001529",
          padding: "0 20px",
          borderRadius: "10px",
        }}
      >
        <Title level={3} style={{ color: "#fff", lineHeight: "20px" }}>
          Inventory Management
        </Title>
      </Header>
      <Content style={{ padding: "20px" }}>
        <InventoryManager />
      </Content>
    </Layout>
  );
};

export default App;
