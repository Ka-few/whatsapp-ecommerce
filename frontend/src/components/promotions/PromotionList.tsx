import React, { useEffect, useState } from 'react';
import { Table, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';

interface Promotion {
  id: number;
  code: string;
  description: string;
  discount_type: string;
  discount_value: number;
  start_date: string;
  end_date: string;
  is_active: boolean;
}

const PromotionList = () => {
  const [promotions, setPromotions] = useState<Promotion[]>([]);

  useEffect(() => {
    fetch('whatsapp-ecommerce-evls.onrender.com/api/promotions/')
      .then(response => response.json())
      .then(data => setPromotions(data));
  }, []);

  const handleDelete = (id: number) => {
    fetch(`whatsapp-ecommerce-evls.onrender.com/api/promotions/${id}/`, {
      method: 'DELETE',
    })
      .then(() => setPromotions(promotions.filter(p => p.id !== id)));
  };

  return (
    <div>
      <h2>Promotions</h2>
      <Link to="/promotions/create" className="btn btn-primary mb-3">Create Promotion</Link>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>#</th>
            <th>Code</th>
            <th>Description</th>
            <th>Discount Type</th>
            <th>Discount Value</th>
            <th>Start Date</th>
            <th>End Date</th>
            <th>Active</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {promotions.map(promotion => (
            <tr key={promotion.id}>
              <td>{promotion.id}</td>
              <td>{promotion.code}</td>
              <td>{promotion.description}</td>
              <td>{promotion.discount_type}</td>
              <td>{promotion.discount_value}</td>
              <td>{new Date(promotion.start_date).toLocaleDateString()}</td>
              <td>{promotion.end_date ? new Date(promotion.end_date).toLocaleDateString() : 'N/A'}</td>
              <td>{promotion.is_active ? 'Yes' : 'No'}</td>
              <td>
                <Link to={`/promotions/edit/${promotion.id}`} className="btn btn-warning btn-sm">Edit</Link>
                <Button variant="danger" size="sm" className="ms-2" onClick={() => handleDelete(promotion.id)}>Delete</Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default PromotionList;
