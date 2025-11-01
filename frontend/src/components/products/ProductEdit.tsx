import React, { useState, useEffect } from 'react';
import { Form, Button } from 'react-bootstrap';
import { useNavigate, useParams } from 'react-router-dom';

const ProductEdit = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [price, setPrice] = useState('');

  useEffect(() => {
    fetch(`whatsapp-ecommerce-evls.onrender.com/api/products/${id}/`)
      .then(response => response.json())
      .then(data => {
        setName(data.name);
        setDescription(data.description);
        setPrice(data.price);
      });
  }, [id]);

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    fetch(`/api/products/${id}/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ name, description, price }),
    })
      .then(response => response.json())
      .then(() => navigate('/products'));
  };

  return (
    <div>
      <h2>Edit Product</h2>
      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="formProductName">
          <Form.Label>Name</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter product name"
            value={name}
            onChange={e => setName(e.target.value)}
          />
        </Form.Group>

        <Form.Group controlId="formProductDescription">
          <Form.Label>Description</Form.Label>
          <Form.Control
            as="textarea"
            rows={3}
            placeholder="Enter product description"
            value={description}
            onChange={e => setDescription(e.target.value)}
          />
        </Form.Group>

        <Form.Group controlId="formProductPrice">
          <Form.Label>Price</Form.Label>
          <Form.Control
            type="number"
            placeholder="Enter product price"
            value={price}
            onChange={e => setPrice(e.target.value)}
          />
        </Form.Group>

        <Button variant="primary" type="submit">
          Update
        </Button>
      </Form>
    </div>
  );
};

export default ProductEdit;
