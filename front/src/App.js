import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { Link } from "react-router-dom";
import { Layout, Menu, ConfigProvider, theme } from "antd";
import { HomeOutlined, TableOutlined, ApartmentOutlined, BarsOutlined } from "@ant-design/icons";
import GetSNInfo from "./components/GetSNInfo";
import ModelTest from "./components/ModelTest";
import Home from "./components/Home";
import MarketPlace from "./components/MarketPlace";
const { Content } = Layout;
const { Footer, Sider } = Layout;

function App() {
  const [collapsed, setCollapsed] = useState(false);
  return (
    <Router>
      <ConfigProvider
        theme={{
          algorithm: theme.darkAlgorithm
        }}
      >
        <Layout
          style={{
            minHeight: "100vh",
          }}
        >
          <Sider
            collapsible
            collapsed={collapsed}
            onCollapse={(value) => setCollapsed(value)}
          >
            <Menu theme="dark" mode="inline">
              <Menu.Item key="1" icon={<HomeOutlined />}>
                <Link to="/">Home</Link>
              </Menu.Item>
              <Menu.Item key="2" icon={<BarsOutlined />}>
                <Link to="/marketplace">MarketPlace</Link>
              </Menu.Item>
              <Menu.Item key="3" icon={<TableOutlined />}>
                <Link to="/getSNInfo">Support Network</Link>
              </Menu.Item>
              <Menu.Item key="4" icon={<ApartmentOutlined />}>
                <Link to="/modelTest">Model Test</Link>
              </Menu.Item>
            </Menu>
          </Sider>
          <Layout>
            <Content
              style={{
                padding: 24,
              }}
            >
              <div
                style={{
                  alignItems: "center",
                  padding: 24,
                  minHeight: 360,
                }}
              >
                <Routes>
                  <Route path="/" element={<Home />} />
                  <Route path="/getSNInfo" element={<GetSNInfo />} />
                  <Route path="/modelTest" element={<ModelTest />} />
                  <Route path="/marketplace" element={<MarketPlace />} />
                </Routes>
              </div>
            </Content>

            <Footer
              style={{
                textAlign: "center",
              }}
            >
              Simulator ©{new Date().getFullYear()} created by Matheus Chagas
            </Footer>
          </Layout>
        </Layout>
      </ConfigProvider>
    </Router>
  );
}

export default App;
