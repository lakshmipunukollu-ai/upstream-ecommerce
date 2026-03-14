import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../store/AuthContext';
import { useCart } from '../store/CartContext';
import { checkout } from '../api';

const Checkout: React.FC = () => {
  const { isAuthenticated } = useAuth();
  const { cart, refreshCart } = useCart();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [form, setForm] = useState({
    line1: '',
    city: '',
    state: '',
    zip: '',
    guest_email: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const data: { shipping_address: Record<string, string>; guest_email?: string } = {
        shipping_address: {
          line1: form.line1,
          city: form.city,
          state: form.state,
          zip: form.zip,
        },
      };
      if (!isAuthenticated && form.guest_email) {
        data.guest_email = form.guest_email;
      }
      const res = await checkout(data);
      // In a real app, we'd use Stripe Elements here.
      // For demo, show order created successfully.
      await refreshCart();
      navigate(`/order-confirmation/${res.data.order_id}`);
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Checkout failed';
      setError(msg);
    }
    setLoading(false);
  };

  if (!cart || cart.items.length === 0) {
    return (
      <div style={{ textAlign: 'center', marginTop: 60 }}>
        <h2>Your cart is empty</h2>
      </div>
    );
  }

  return (
    <div style={{ maxWidth: 600, margin: '0 auto' }}>
      <h1 style={{ fontSize: 28, marginBottom: 20 }}>Checkout</h1>

      <div style={styles.summary}>
        <h3>Order Summary</h3>
        {cart.items.map((item) => (
          <div key={item.id} style={styles.summaryItem}>
            <span>{item.product.title} x{item.quantity}</span>
            <span>${item.subtotal}</span>
          </div>
        ))}
        <div style={styles.summaryTotal}>
          <strong>Total</strong>
          <strong>${cart.total}</strong>
        </div>
      </div>

      <form onSubmit={handleSubmit}>
        {!isAuthenticated && (
          <div style={styles.field}>
            <label style={styles.label}>Email</label>
            <input
              name="guest_email"
              type="email"
              value={form.guest_email}
              onChange={handleChange}
              required
              style={styles.input}
              placeholder="your@email.com"
            />
          </div>
        )}
        <h3 style={{ marginTop: 20, marginBottom: 12 }}>Shipping Address</h3>
        <div style={styles.field}>
          <label style={styles.label}>Address Line</label>
          <input name="line1" value={form.line1} onChange={handleChange} required style={styles.input} />
        </div>
        <div style={{ display: 'flex', gap: 12 }}>
          <div style={{ ...styles.field, flex: 2 }}>
            <label style={styles.label}>City</label>
            <input name="city" value={form.city} onChange={handleChange} required style={styles.input} />
          </div>
          <div style={{ ...styles.field, flex: 1 }}>
            <label style={styles.label}>State</label>
            <input name="state" value={form.state} onChange={handleChange} required style={styles.input} maxLength={2} />
          </div>
          <div style={{ ...styles.field, flex: 1 }}>
            <label style={styles.label}>ZIP</label>
            <input name="zip" value={form.zip} onChange={handleChange} required style={styles.input} />
          </div>
        </div>

        {error && <p style={{ color: '#e53e3e', marginTop: 12 }}>{error}</p>}

        <button type="submit" disabled={loading} style={styles.submitBtn}>
          {loading ? 'Processing...' : 'Place Order'}
        </button>
        <p style={{ fontSize: 12, color: '#718096', marginTop: 8, textAlign: 'center' }}>
          Demo mode - no real payment will be charged
        </p>
      </form>
    </div>
  );
};

const styles: Record<string, React.CSSProperties> = {
  summary: {
    background: '#fff',
    border: '1px solid #e2e8f0',
    borderRadius: 8,
    padding: 16,
    marginBottom: 24,
  },
  summaryItem: { display: 'flex', justifyContent: 'space-between', padding: '4px 0', fontSize: 14 },
  summaryTotal: {
    display: 'flex',
    justifyContent: 'space-between',
    borderTop: '1px solid #e2e8f0',
    paddingTop: 8,
    marginTop: 8,
    fontSize: 16,
  },
  field: { marginBottom: 12 },
  label: { display: 'block', fontSize: 13, fontWeight: 600, marginBottom: 4, color: '#4a5568' },
  input: {
    width: '100%',
    padding: '10px 12px',
    border: '1px solid #e2e8f0',
    borderRadius: 6,
    fontSize: 14,
    boxSizing: 'border-box',
  },
  submitBtn: {
    width: '100%',
    padding: '14px 24px',
    background: '#38a169',
    color: '#fff',
    border: 'none',
    borderRadius: 6,
    fontWeight: 'bold',
    fontSize: 16,
    cursor: 'pointer',
    marginTop: 16,
  },
};

export default Checkout;
