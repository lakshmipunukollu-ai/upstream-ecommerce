import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getProduct } from '../api';
import { useCart } from '../store/CartContext';
import type { Product } from '../types';

const ProductDetail: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const [product, setProduct] = useState<Product | null>(null);
  const [quantity, setQuantity] = useState(1);
  const [adding, setAdding] = useState(false);
  const [message, setMessage] = useState('');
  const { addItem } = useCart();
  const navigate = useNavigate();

  useEffect(() => {
    if (slug) {
      getProduct(slug).then((res) => setProduct(res.data));
    }
  }, [slug]);

  if (!product) return <p>Loading...</p>;

  const handleAdd = async () => {
    setAdding(true);
    try {
      await addItem(product.id, quantity);
      setMessage('Added to cart!');
      setTimeout(() => setMessage(''), 2000);
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Error adding to cart';
      setMessage(msg);
    }
    setAdding(false);
  };

  return (
    <div style={styles.container}>
      <button onClick={() => navigate(-1)} style={styles.back}>Back</button>
      <div style={styles.layout}>
        <div style={styles.imageBox}>
          <div style={styles.placeholder}>{product.title[0]}</div>
        </div>
        <div style={styles.info}>
          <span style={styles.category}>{product.category.name}</span>
          <h1 style={styles.title}>{product.title}</h1>
          <div style={styles.grades}>
            {product.grade_levels.map((g) => (
              <span key={g} style={styles.grade}>Grade {g}</span>
            ))}
          </div>
          <p style={styles.price}>${product.price}</p>
          <p style={{ color: product.stock > 0 ? '#38a169' : '#e53e3e' }}>
            {product.stock > 0 ? `${product.stock} in stock` : 'Out of stock'}
          </p>
          <p style={styles.description}>{product.description}</p>

          {product.stock > 0 && (
            <div style={styles.addRow}>
              <input
                type="number"
                min={1}
                max={product.stock}
                value={quantity}
                onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value) || 1))}
                style={styles.qtyInput}
              />
              <button onClick={handleAdd} disabled={adding} style={styles.addBtn}>
                {adding ? 'Adding...' : 'Add to Cart'}
              </button>
            </div>
          )}
          {message && <p style={{ color: '#38a169', marginTop: 8 }}>{message}</p>}
        </div>
      </div>
    </div>
  );
};

const styles: Record<string, React.CSSProperties> = {
  container: { maxWidth: 900, margin: '0 auto' },
  back: {
    background: 'transparent',
    border: 'none',
    color: '#3182ce',
    cursor: 'pointer',
    fontSize: 14,
    marginBottom: 16,
    padding: 0,
  },
  layout: { display: 'flex', gap: 40, flexWrap: 'wrap' },
  imageBox: {
    flex: '0 0 350px',
    height: 300,
    background: '#edf2f7',
    borderRadius: 8,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  placeholder: { fontSize: 72, fontWeight: 'bold', color: '#a0aec0' },
  info: { flex: 1, minWidth: 280 },
  category: { fontSize: 13, color: '#718096', textTransform: 'uppercase', letterSpacing: 1 },
  title: { fontSize: 28, margin: '8px 0 12px' },
  grades: { display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 16 },
  grade: {
    background: '#ebf8ff',
    color: '#2b6cb0',
    fontSize: 12,
    padding: '3px 10px',
    borderRadius: 12,
  },
  price: { fontSize: 28, fontWeight: 'bold', color: '#2d3748', margin: '8px 0' },
  description: { lineHeight: 1.6, color: '#4a5568', marginTop: 16 },
  addRow: { display: 'flex', gap: 12, marginTop: 20 },
  qtyInput: {
    width: 60,
    padding: '8px 12px',
    border: '1px solid #e2e8f0',
    borderRadius: 6,
    fontSize: 14,
    textAlign: 'center',
  },
  addBtn: {
    padding: '10px 24px',
    background: '#ed8936',
    color: '#fff',
    border: 'none',
    borderRadius: 6,
    fontWeight: 'bold',
    cursor: 'pointer',
    fontSize: 14,
  },
};

export default ProductDetail;
