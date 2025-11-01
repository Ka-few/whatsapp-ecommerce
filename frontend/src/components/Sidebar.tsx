import React from 'react';
import { Nav } from 'react-bootstrap';
import { NavLink } from 'react-router-dom';

const Sidebar = () => {
  return (
    <Nav className="bg-success sidebar flex-column p-2 flex-grow-1">
      <h3 className="text-white text-center mt-3 mb-4">Admin Dashboard</h3>
      <Nav.Item>
        <NavLink to="/products" className={({ isActive }) => "nav-link w-100" + (isActive ? " active" : "")}>Products</NavLink>
      </Nav.Item>
      <Nav.Item>
        <NavLink to="/orders" className={({ isActive }) => "nav-link w-100" + (isActive ? " active" : "")}>Orders</NavLink>
      </Nav.Item>
      <Nav.Item>
        <NavLink to="/promotions" className={({ isActive }) => "nav-link w-100" + (isActive ? " active" : "")}>Promotions</NavLink>
      </Nav.Item>
      <Nav.Item>
        <NavLink to="/users" className={({ isActive }) => "nav-link w-100" + (isActive ? " active" : "")}>Users</NavLink>
      </Nav.Item>
      <Nav.Item>
        <NavLink to="/analytics" className={({ isActive }) => "nav-link w-100" + (isActive ? " active" : "")}>Analytics</NavLink>
      </Nav.Item>
    </Nav>
  );
};

export default Sidebar;
