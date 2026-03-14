import React, { useEffect, useState } from 'react';
import { getRecommendations } from '../api';
import { useCart } from '../store/CartContext';
import type { Recommendation } from '../types';

const Recommendations: React.FC = () => {
  const [recs, setRecs] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { addItem } = useCart();
  const [addingId, setAddingId] = useState<string | null>(null);

  useEffect(() => {
    getRecommendations()
      .then((res) => setRecs(res.data.recommendations))
      .catch((err) => setError(err?.response?.data?.detail || 'Failed to load recommendations'))
      .finally(() => setLoading(false));
  }, []);

  const handleAdd = async (productId: string) => {
    setAddingId(productId);
    try {
      await addItem(productId, 1);
    } catch {
      // ignore
    }
    setAddingId(null);
  };

  if (loading) return <p>Loading recommendations...</p>;
  if (error) return <p style={{ color: '#e53e3e' }}>{error}</p>;

  return (
    <div>
      <h1 style={{ fontSize: 28, marginBottom: 8 }}>AI Recommendations</h1>
      <p style={{ color: '#718096', marginBottom: 24 }}>
        Personalized product suggestions based on your district profile and purchase history.
      </p>

      {recs.length === 0 ? (
        <p style={{ textAlign: 'center', color: '#718096', marginTop: 40 }}>
          No recommendations available. Try updating your district profile.
        </p>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
          {recs.map((rec) => (
            <div key={rec.product.id} style={styles.card}>
              <div style={{ flex: 1 }}>
                <h3 style={styles.title}>{rec.product.title}</h3>
                <p style={styles.reason}>{rec.reason}</p>
                <div style={styles.meta}>
                  <span style={styles.price}>${rec.product.price}</span>
                  <span style={styles.confidence}>
                    Confidence: {Math.round(rec.confidence * 100)}%
                  </span>
                  <span style={styles.grades}>
                    Grades: {rec.grade_levels_served.join(', ')}
                  </span>
                </div>
              </div>
              <button
                onClick={() => handleAdd(rec.product.id)}
                disabled={addingId === rec.product.id}
                style={styles.addBtn}
              >
                {addingId === rec.product.id ? 'Adding...' : 'Add to Cart'}
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

const styles: Record<string, React.CSSProperties> = {
  card: {
    display: 'flex',
    alignItems: 'center',
    gap: 20,
    background: '#fff',
    border: '1px solid #e2e8f0',
    borderRadius: 8,
    padding: 20,
    flexWrap: 'wrap',
  },
  title: { margin: '0 0 8px', fontSize: 18 },
  reason: { color: '#4a5568', fontSize: 14, margin: '0 0 12px' },
  meta: { display: 'flex', gap: 16, flexWrap: 'wrap' },
  price: { fontWeight: 'bold', fontSize: 16, color: '#2d3748' },
  confidence: { fontSize: 13, color: '#718096' },
  grades: { fontSize: 13, color: '#3182ce' },
  addBtn: {
    padding: '10px 20px',
    background: '#ed8936',
    color: '#fff',
    border: 'none',
    borderRadius: 6,
    fontWeight: 'bold',
    cursor: 'pointer',
    whiteSpace: 'nowrap',
  },
};

export default Recommendations;
