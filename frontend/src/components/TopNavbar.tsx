import React from 'react';
import { Navbar, Container, Nav } from 'react-bootstrap';
import { NavLink } from 'react-router-dom';

const TopNavbar = () => {
  return (
    <Navbar bg="success" variant="dark" sticky="top" className="flex-md-nowrap p-0 shadow">
      <Container fluid>
        <Navbar.Brand href="#home" className="px-3 fs-6 text-white">
          WhatsApp E-commerce Admin
        </Navbar.Brand>
        <Nav className="d-none d-md-flex me-auto">
          <NavLink to="/products" className="nav-link text-white">Products</NavLink>
          <NavLink to="/orders" className="nav-link text-white">Orders</NavLink>
          <NavLink to="/users" className="nav-link text-white">Users</NavLink>
          <NavLink to="/promotions" className="nav-link text-white">Promotions</NavLink>
          <NavLink to="/analytics" className="nav-link text-white">Analytics</NavLink>
        </Nav>
      </Container>
    </Navbar>
  );
};

export default TopNavbar;
