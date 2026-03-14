import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getProducts } from '../api';
import ProductCard from '../components/ProductCard';
import type { Product } from '../types';

const Home: React.FC = () => {
  const [products, setProducts] = useState<Product[]>([]);

  useEffect(() => {
    getProducts({ page: '1' }).then((res) => setProducts(res.data.results.slice(0, 6)));
  }, []);

  return (
    <div>
      <section style={styles.hero}>
        <h1 style={styles.heroTitle}>Upstream Literacy</h1>
        <p style={styles.heroSub}>
          Research-based literacy curriculum and materials for K-8 educators and school districts.
        </p>
        <Link to="/products" style={styles.heroBtn}>Browse Products</Link>
      </section>

      <section style={{ marginTop: 48 }}>
        <h2 style={styles.sectionTitle}>Featured Products</h2>
        <div style={styles.grid}>
          {products.map((p) => (
            <ProductCard key={p.id} product={p} />
          ))}
        </div>
      </section>
    </div>
  );
};

const styles: Record<string, React.CSSProperties> = {
  hero: {
    textAlign: 'center',
    padding: '60px 20px',
    background: 'linear-gradient(135deg, #1a365d 0%, #2a4365 100%)',
    borderRadius: 12,
    color: '#fff',
  },
  heroTitle: { fontSize: 42, margin: 0 },
  heroSub: { fontSize: 18, marginTop: 12, color: '#bee3f8', maxWidth: 600, marginLeft: 'auto', marginRight: 'auto' },
  heroBtn: {
    display: 'inline-block',
    marginTop: 24,
    padding: '12px 32px',
    background: '#ed8936',
    color: '#fff',
    borderRadius: 6,
    textDecoration: 'none',
    fontWeight: 'bold',
    fontSize: 16,
  },
  sectionTitle: { fontSize: 24, marginBottom: 20 },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
    gap: 24,
  },
};

export default Home;
