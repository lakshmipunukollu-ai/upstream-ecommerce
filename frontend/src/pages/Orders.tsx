import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getOrders } from '../api';
import type { Order } from '../types';

const statusColors: Record<string, string> = {
  pending: '#ed8936',
  paid: '#38a169',
  shipped: '#3182ce',
  delivered: '#2d3748',
  cancelled: '#e53e3e',
};

const Orders: React.FC = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getOrders()
      .then((res) => setOrders(res.data.results))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Loading orders...</p>;

  return (
    <div>
      <h1 style={{ fontSize: 28, marginBottom: 20 }}>Order History</h1>
      {orders.length === 0 ? (
        <p style={{ textAlign: 'center', color: '#718096', marginTop: 40 }}>
          No orders yet. <Link to="/products" style={{ color: '#3182ce' }}>Start shopping</Link>
        </p>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {orders.map((order) => (
            <div key={order.id} style={styles.card}>
              <div style={styles.header}>
                <div>
                  <span style={styles.orderId}>Order #{order.id.slice(0, 8)}</span>
                  <span style={{ ...styles.status, background: statusColors[order.status] || '#718096' }}>
                    {order.status}
                  </span>
                </div>
                <span style={styles.date}>
                  {new Date(order.created_at).toLocaleDateString()}
                </span>
              </div>
              <div style={styles.items}>
                {order.items.map((item) => (
                  <div key={item.id} style={styles.item}>
                    <span>{item.product.title} x{item.quantity}</span>
                    <span>${item.subtotal}</span>
                  </div>
                ))}
              </div>
              <div style={styles.total}>Total: ${order.total}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

const styles: Record<string, React.CSSProperties> = {
  card: {
    background: '#fff',
    border: '1px solid #e2e8f0',
    borderRadius: 8,
    padding: 16,
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  orderId: { fontWeight: 600, marginRight: 12 },
  status: {
    fontSize: 12,
    padding: '3px 10px',
    borderRadius: 12,
    color: '#fff',
    textTransform: 'capitalize',
  },
  date: { fontSize: 13, color: '#718096' },
  items: { borderTop: '1px solid #f0f0f0', paddingTop: 8 },
  item: {
    display: 'flex',
    justifyContent: 'space-between',
    padding: '4px 0',
    fontSize: 14,
  },
  total: {
    borderTop: '1px solid #f0f0f0',
    paddingTop: 8,
    marginTop: 8,
    fontWeight: 'bold',
    textAlign: 'right',
  },
};

export default Orders;
