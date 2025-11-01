import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Sidebar from './Sidebar';
import ProductList from './products/ProductList';
import ProductCreate from './products/ProductCreate';
import ProductEdit from './products/ProductEdit';
import OrderList from './orders/OrderList';
import UserList from './users/UserList';
import PromotionList from './promotions/PromotionList';
import PromotionCreate from './promotions/PromotionCreate';
import PromotionEdit from './promotions/PromotionEdit';
import Analytics from './analytics/Analytics';

const Dashboard = () => {
  return (
    <Router>
      <div className="container-fluid">
        <div className="row">
          <div className="col-md-2 d-none d-md-block bg-light sidebar">
            <Sidebar />
          </div>
          <main role="main" className="col-md-10 ml-sm-auto px-4 main-content">
            <Routes>
              <Route path="/" element={<Navigate to="/products" replace />} />
              <Route path="/products" element={<ProductList />} />
              <Route path="/products/create" element={<ProductCreate />} />
              <Route path="/products/edit/:id" element={<ProductEdit />} />
              <Route path="/orders" element={<OrderList />} />
              <Route path="/users" element={<UserList />} />
              <Route path="/promotions" element={<PromotionList />} />
              <Route path="/promotions/create" element={<PromotionCreate />} />
              <Route path="/promotions/edit/:id" element={<PromotionEdit />} />
              <Route path="/analytics" element={<Analytics />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
};

export default Dashboard;
