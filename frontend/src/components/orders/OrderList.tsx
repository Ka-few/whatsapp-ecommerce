import React, { useEffect, useState } from 'react';
import { Table } from 'react-bootstrap';
import { API_BASE_URL } from '../../apiConfig';

interface Order {
  id: number;
  user: {
    phone_number: string;
  };
  total_amount: number;
  status: string;
  created_at: string;
}

const OrderList = () => {
  const [orders, setOrders] = useState<Order[]>([]);

  useEffect(() => {
    fetch(`${API_BASE_URL}/orders/`)
      .then(response => response.json())
      .then(data => setOrders(data));
  }, []);

  return (
    <div>
      <h2>Orders</h2>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>#</th>
            <th>User</th>
            <th>Total Amount</th>
            <th>Status</th>
            <th>Created At</th>
          </tr>
        </thead>
        <tbody>
          {orders.map(order => (
            <tr key={order.id}>
              <td>{order.id}</td>
              <td>{order.user.phone_number}</td>
              <td>{order.total_amount}</td>
              <td>{order.status}</td>
              <td>{new Date(order.created_at).toLocaleDateString()}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default OrderList;
