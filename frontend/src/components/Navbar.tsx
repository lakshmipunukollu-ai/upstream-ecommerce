import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../store/AuthContext';
import { useCart } from '../store/CartContext';

const Navbar: React.FC = () => {
  const { user, isAuthenticated, isAdmin, logout } = useAuth();
  const { cart } = useCart();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav style={styles.nav}>
      <div style={styles.container}>
        <Link to="/" style={styles.brand}>Upstream Literacy</Link>
        <div style={styles.links}>
          <Link to="/products" style={styles.link}>Products</Link>
          <Link to="/cart" style={styles.link}>
            Cart {cart && cart.item_count > 0 && `(${cart.item_count})`}
          </Link>
          {isAuthenticated ? (
            <>
              <Link to="/orders" style={styles.link}>Orders</Link>
              <Link to="/recommendations" style={styles.link}>Recommendations</Link>
              {isAdmin && <Link to="/inventory" style={styles.link}>Inventory</Link>}
              <Link to="/profile" style={styles.link}>{user?.first_name}</Link>
              <button onClick={handleLogout} style={styles.button}>Logout</button>
            </>
          ) : (
            <>
              <Link to="/login" style={styles.link}>Login</Link>
              <Link to="/register" style={styles.link}>Register</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

const styles: Record<string, React.CSSProperties> = {
  nav: {
    background: '#1a365d',
    padding: '0 20px',
    position: 'sticky',
    top: 0,
    zIndex: 100,
  },
  container: {
    maxWidth: 1200,
    margin: '0 auto',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    height: 60,
  },
  brand: {
    color: '#fff',
    fontSize: 20,
    fontWeight: 'bold',
    textDecoration: 'none',
  },
  links: {
    display: 'flex',
    alignItems: 'center',
    gap: 16,
  },
  link: {
    color: '#e2e8f0',
    textDecoration: 'none',
    fontSize: 14,
  },
  button: {
    background: 'transparent',
    border: '1px solid #e2e8f0',
    color: '#e2e8f0',
    padding: '6px 12px',
    borderRadius: 4,
    cursor: 'pointer',
    fontSize: 14,
  },
};

export default Navbar;
