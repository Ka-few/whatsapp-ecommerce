import React, { useEffect, useState } from 'react';
import { Table, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';

interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
}

const ProductList = () => {
  const [products, setProducts] = useState<Product[]>([]);

  useEffect(() => {
    fetch('/api/products/')
      .then(response => response.json())
      .then(data => setProducts(data));
  }, []);

  const handleDelete = (id: number) => {
    fetch(`/api/products/${id}/`, {
      method: 'DELETE',
    })
      .then(() => setProducts(products.filter(p => p.id !== id)));
  };

  return (
    <div>
      <h2>Products</h2>
      <Link to="/products/create" className="btn btn-primary mb-3">Create Product</Link>
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>#</th>
            <th>Name</th>
            <th>Description</th>
            <th>Price</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {products.map(product => (
            <tr key={product.id}>
              <td>{product.id}</td>
              <td>{product.name}</td>
              <td>{product.description}</td>
              <td>{product.price}</td>
              <td>
                <Link to={`/products/edit/${product.id}`} className="btn btn-warning btn-sm">Edit</Link>
                <Button variant="danger" size="sm" className="ms-2" onClick={() => handleDelete(product.id)}>Delete</Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default ProductList;