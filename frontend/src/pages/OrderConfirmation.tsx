import React from 'react';
import { useParams, Link } from 'react-router-dom';

const OrderConfirmation: React.FC = () => {
  const { orderId } = useParams<{ orderId: string }>();

  return (
    <div style={{ textAlign: 'center', marginTop: 60 }}>
      <div style={{ fontSize: 48, marginBottom: 16 }}>&#10003;</div>
      <h1 style={{ fontSize: 28, marginBottom: 12 }}>Order Placed!</h1>
      <p style={{ color: '#718096', marginBottom: 8 }}>
        Your order has been created. Order ID:
      </p>
      <p style={{ fontFamily: 'monospace', fontSize: 14, color: '#4a5568', marginBottom: 24 }}>
        {orderId}
      </p>
      <p style={{ color: '#718096', marginBottom: 24 }}>
        In a production environment, payment would be processed via Stripe.
      </p>
      <div style={{ display: 'flex', gap: 16, justifyContent: 'center' }}>
        <Link to="/products" style={styles.link}>Continue Shopping</Link>
        <Link to="/orders" style={styles.linkAlt}>View Orders</Link>
      </div>
    </div>
  );
};

const styles: Record<string, React.CSSProperties> = {
  link: {
    padding: '10px 24px',
    background: '#3182ce',
    color: '#fff',
    borderRadius: 6,
    textDecoration: 'none',
    fontWeight: 'bold',
  },
  linkAlt: {
    padding: '10px 24px',
    border: '1px solid #3182ce',
    color: '#3182ce',
    borderRadius: 6,
    textDecoration: 'none',
    fontWeight: 'bold',
  },
};

export default OrderConfirmation;
