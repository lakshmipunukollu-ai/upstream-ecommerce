import React from 'react';
import { Link } from 'react-router-dom';
import type { Product } from '../types';

interface Props {
  product: Product;
}

const ProductCard: React.FC<Props> = ({ product }) => {
  return (
    <Link to={`/products/${product.slug}`} style={styles.card}>
      <div style={styles.imageBox}>
        <div style={styles.placeholder}>{product.title[0]}</div>
      </div>
      <div style={styles.body}>
        <div style={styles.category}>{product.category.name}</div>
        <h3 style={styles.title}>{product.title}</h3>
        <div style={styles.grades}>
          {product.grade_levels.map((g) => (
            <span key={g} style={styles.grade}>Grade {g}</span>
          ))}
        </div>
        <div style={styles.footer}>
          <span style={styles.price}>${product.price}</span>
          <span style={{ color: product.stock > 0 ? '#38a169' : '#e53e3e', fontSize: 13 }}>
            {product.stock > 0 ? `${product.stock} in stock` : 'Out of stock'}
          </span>
        </div>
      </div>
    </Link>
  );
};

const styles: Record<string, React.CSSProperties> = {
  card: {
    border: '1px solid #e2e8f0',
    borderRadius: 8,
    overflow: 'hidden',
    textDecoration: 'none',
    color: 'inherit',
    display: 'flex',
    flexDirection: 'column',
    transition: 'box-shadow 0.2s',
  },
  imageBox: {
    background: '#edf2f7',
    height: 160,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  placeholder: {
    fontSize: 48,
    fontWeight: 'bold',
    color: '#a0aec0',
  },
  body: { padding: 16, flex: 1, display: 'flex', flexDirection: 'column' },
  category: { fontSize: 12, color: '#718096', textTransform: 'uppercase', letterSpacing: 1 },
  title: { margin: '8px 0', fontSize: 16, fontWeight: 600 },
  grades: { display: 'flex', flexWrap: 'wrap', gap: 4, marginBottom: 12 },
  grade: {
    background: '#ebf8ff',
    color: '#2b6cb0',
    fontSize: 11,
    padding: '2px 8px',
    borderRadius: 12,
  },
  footer: {
    marginTop: 'auto',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  price: { fontSize: 18, fontWeight: 'bold', color: '#2d3748' },
};

export default ProductCard;
