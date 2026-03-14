import React from 'react';
import { Link } from 'react-router-dom';
import { useCart } from '../store/CartContext';

const CartPage: React.FC = () => {
  const { cart, loading, updateItem, removeItem, clearCart } = useCart();

  if (loading) return <p>Loading cart...</p>;
  if (!cart || cart.items.length === 0) {
    return (
      <div style={{ textAlign: 'center', marginTop: 60 }}>
        <h2>Your cart is empty</h2>
        <Link to="/products" style={styles.shopLink}>Browse Products</Link>
      </div>
    );
  }

  return (
    <div>
      <h1 style={{ fontSize: 28, marginBottom: 20 }}>Shopping Cart</h1>
      <div style={styles.items}>
        {cart.items.map((item) => (
          <div key={item.id} style={styles.item}>
            <div style={{ flex: 1 }}>
              <Link to={`/products/${item.product.slug}`} style={styles.productName}>
                {item.product.title}
              </Link>
              <p style={styles.meta}>{item.product.category.name} | ${item.product.price} each</p>
            </div>
            <div style={styles.qtyBox}>
              <button
                onClick={() => updateItem(item.id, item.quantity - 1)}
                style={styles.qtyBtn}
              >
                -
              </button>
              <span style={styles.qty}>{item.quantity}</span>
              <button
                onClick={() => updateItem(item.id, item.quantity + 1)}
                style={styles.qtyBtn}
              >
                +
              </button>
            </div>
            <div style={styles.subtotal}>${item.subtotal}</div>
            <button onClick={() => removeItem(item.id)} style={styles.removeBtn}>Remove</button>
          </div>
        ))}
      </div>

      <div style={styles.footer}>
        <button onClick={clearCart} style={styles.clearBtn}>Clear Cart</button>
        <div style={{ textAlign: 'right' }}>
          <p style={styles.total}>Total: ${cart.total}</p>
          <Link to="/checkout" style={styles.checkoutBtn}>Proceed to Checkout</Link>
        </div>
      </div>
    </div>
  );
};

const styles: Record<string, React.CSSProperties> = {
  shopLink: { color: '#3182ce', display: 'inline-block', marginTop: 12 },
  items: { display: 'flex', flexDirection: 'column', gap: 12 },
  item: {
    display: 'flex',
    alignItems: 'center',
    gap: 20,
    padding: 16,
    background: '#fff',
    borderRadius: 8,
    border: '1px solid #e2e8f0',
    flexWrap: 'wrap',
  },
  productName: { fontWeight: 600, fontSize: 16, color: '#2d3748', textDecoration: 'none' },
  meta: { fontSize: 13, color: '#718096', marginTop: 4 },
  qtyBox: { display: 'flex', alignItems: 'center', gap: 8 },
  qtyBtn: {
    width: 30,
    height: 30,
    border: '1px solid #e2e8f0',
    borderRadius: 4,
    background: '#fff',
    cursor: 'pointer',
    fontSize: 16,
  },
  qty: { fontSize: 16, minWidth: 24, textAlign: 'center' },
  subtotal: { fontSize: 16, fontWeight: 'bold', minWidth: 80, textAlign: 'right' },
  removeBtn: {
    background: 'transparent',
    border: 'none',
    color: '#e53e3e',
    cursor: 'pointer',
    fontSize: 13,
  },
  footer: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-end',
    marginTop: 24,
    flexWrap: 'wrap',
    gap: 16,
  },
  clearBtn: {
    padding: '8px 16px',
    border: '1px solid #e2e8f0',
    borderRadius: 6,
    background: '#fff',
    cursor: 'pointer',
    fontSize: 14,
  },
  total: { fontSize: 22, fontWeight: 'bold', marginBottom: 12 },
  checkoutBtn: {
    display: 'inline-block',
    padding: '12px 32px',
    background: '#38a169',
    color: '#fff',
    borderRadius: 6,
    textDecoration: 'none',
    fontWeight: 'bold',
    fontSize: 16,
  },
};

export default CartPage;
