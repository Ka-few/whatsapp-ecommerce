import React, { useEffect, useState } from 'react';
import { Card, Row, Col } from 'react-bootstrap';

interface AnalyticsData {
  totalProducts: number;
  totalOrders: number;
  totalUsers: number;
  totalRevenue: number;
}

const Analytics = () => {
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);

  useEffect(() => {
    fetch('https://whatsapp-ecommerce-evls.onrender.com/api/analytics/')
      .then(response => response.json())
      .then(data => setAnalytics(data))
      .catch(error => console.error('Error fetching analytics:', error));
  }, []);

  if (!analytics) {
    return <div>Loading Analytics...</div>;
  }

  return (
    <div>
      <h2>Analytics Dashboard</h2>
      <Row>
        <Col md={3}>
          <Card bg="success" text="white" className="mb-4">
            <Card.Body>
              <Card.Title>{analytics.totalProducts}</Card.Title>
              <Card.Text>Total Products</Card.Text>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card bg="info" text="white" className="mb-4">
            <Card.Body>
              <Card.Title>{analytics.totalOrders}</Card.Title>
              <Card.Text>Total Orders</Card.Text>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card bg="warning" text="dark" className="mb-4">
            <Card.Body>
              <Card.Title>{analytics.totalUsers}</Card.Title>
              <Card.Text>Total Users</Card.Text>
            </Card.Body>
          </Card>
        </Col>
        <Col md={3}>
          <Card bg="danger" text="white" className="mb-4">
            <Card.Body>
              <Card.Title>KES {analytics.totalRevenue.toLocaleString()}</Card.Title>
              <Card.Text>Total Revenue</Card.Text>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Analytics;
