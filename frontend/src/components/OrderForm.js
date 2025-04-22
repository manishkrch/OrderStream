import React, { useState } from 'react';
import axios from 'axios';

const OrderForm = () => {
  const [form, setForm] = useState({
    customer_name: '',
    item: '',
    quantity: 1
  });

  const [status, setStatus] = useState('');

  const handleChange = e => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      const res = await axios.post("http://api-gateway:8000/orders", form);
      setStatus('✅ Order submitted successfully!');
      console.log(res.data);
    } catch (err) {
      console.error(err);
      setStatus('❌ Failed to submit order');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Name:</label>
        <input name="customer_name" value={form.customer_name} onChange={handleChange} required />
      </div>
      <div>
        <label>Item:</label>
        <input name="item" value={form.item} onChange={handleChange} required />
      </div>
      <div>
        <label>Quantity:</label>
        <input name="quantity" type="number" value={form.quantity} onChange={handleChange} required min="1" />
      </div>
      <button type="submit">Place Order</button>
      <p>{status}</p>
    </form>
  );
};

export default OrderForm;
