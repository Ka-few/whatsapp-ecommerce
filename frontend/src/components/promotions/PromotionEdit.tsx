import React, { useState, useEffect } from 'react';
import { Form, Button } from 'react-bootstrap';
import { useNavigate, useParams } from 'react-router-dom';
import { API_BASE_URL } from '../../apiConfig';

const PromotionEdit = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [code, setCode] = useState('');
  const [description, setDescription] = useState('');
  const [discountType, setDiscountType] = useState('percentage');
  const [discountValue, setDiscountValue] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [isActive, setIsActive] = useState(true);

  useEffect(() => {
    fetch(`${API_BASE_URL}/promotions/${id}/`)
      .then(response => response.json())
      .then(data => {
        setCode(data.code);
        setDescription(data.description);
        setDiscountType(data.discount_type);
        setDiscountValue(data.discount_value);
        setStartDate(data.start_date.slice(0, 16));
        setEndDate(data.end_date ? data.end_date.slice(0, 16) : '');
        setIsActive(data.is_active);
      });
  }, [id]);

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    fetch(`${API_BASE_URL}/promotions/${id}/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        code,
        description,
        discount_type: discountType,
        discount_value: discountValue,
        start_date: startDate,
        end_date: endDate,
        is_active: isActive,
      }),
    })
      .then(response => response.json())
      .then(() => navigate('/promotions'));
  };

  return (
    <div>
      <h2>Edit Promotion</h2>
      <Form onSubmit={handleSubmit}>
        <Form.Group controlId="formPromotionCode">
          <Form.Label>Code</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter promotion code"
            value={code}
            onChange={e => setCode(e.target.value)}
          />
        </Form.Group>

        <Form.Group controlId="formPromotionDescription">
          <Form.Label>Description</Form.Label>
          <Form.Control
            as="textarea"
            rows={3}
            placeholder="Enter promotion description"
            value={description}
            onChange={e => setDescription(e.target.value)}
          />
        </Form.Group>

        <Form.Group controlId="formPromotionDiscountType">
          <Form.Label>Discount Type</Form.Label>
          <Form.Control
            as="select"
            value={discountType}
            onChange={e => setDiscountType(e.target.value)}
          >
            <option value="percentage">Percentage</option>
            <option value="fixed">Fixed Amount</option>
          </Form.Control>
        </Form.Group>

        <Form.Group controlId="formPromotionDiscountValue">
          <Form.Label>Discount Value</Form.Label>
          <Form.Control
            type="number"
            placeholder="Enter discount value"
            value={discountValue}
            onChange={e => setDiscountValue(e.target.value)}
          />
        </Form.Group>

        <Form.Group controlId="formPromotionStartDate">
          <Form.Label>Start Date</Form.Label>
          <Form.Control
            type="datetime-local"
            value={startDate}
            onChange={e => setStartDate(e.target.value)}
          />
        </Form.Group>

        <Form.Group controlId="formPromotionEndDate">
          <Form.Label>End Date</Form.Label>
          <Form.Control
            type="datetime-local"
            value={endDate}
            onChange={e => setEndDate(e.target.value)}
          />
        </Form.Group>

        <Form.Group controlId="formPromotionIsActive">
          <Form.Check
            type="checkbox"
            label="Active"
            checked={isActive}
            onChange={e => setIsActive(e.target.checked)}
          />
        </Form.Group>

        <Button variant="primary" type="submit">
          Update
        </Button>
      </Form>
    </div>
  );
};

export default PromotionEdit;
