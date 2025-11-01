import React, { useEffect, useState } from 'react';
import { Table } from 'react-bootstrap';

interface User {
  id: number;
  phone_number: string;
  name: string;
  email: string;
  total_referrals: number;
  total_commission: number;
}

const UserList = () => {
  const [users, setUsers] = useState<User[]>([]);

  useEffect(() => {
    fetch('/api/users/')
      .then(response => response.json())
      .then(data => setUsers(data));
  }, []);

  return (
    <div>
      <h2>Users</h2>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>#</th>
            <th>Phone Number</th>
            <th>Name</th>
            <th>Email</th>
            <th>Total Referrals</th>
            <th>Total Commission</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id}>
              <td>{user.id}</td>
              <td>{user.phone_number}</td>
              <td>{user.name}</td>
              <td>{user.email}</td>
              <td>{user.total_referrals}</td>
              <td>{user.total_commission}</td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default UserList;
