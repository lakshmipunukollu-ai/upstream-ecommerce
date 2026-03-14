import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { register } from '../api';
import { useAuth } from '../store/AuthContext';

const Register: React.FC = () => {
  const [form, setForm] = useState({
    email: '',
    password: '',
    first_name: '',
    last_name: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { setTokens } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const res = await register(form);
      setTokens(res.data.tokens.access, res.data.tokens.refresh);
      navigate('/');
    } catch (err: unknown) {
      const data = (err as { response?: { data?: Record<string, string[]> } })?.response?.data;
      if (data) {
        const msgs = Object.values(data).flat();
        setError(msgs.join(', '));
      } else {
        setError('Registration failed');
      }
    }
    setLoading(false);
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Create Account</h1>
      <form onSubmit={handleSubmit} style={styles.form}>
        <div style={{ display: 'flex', gap: 12 }}>
          <div style={{ ...styles.field, flex: 1 }}>
            <label style={styles.label}>First Name</label>
            <input name="first_name" value={form.first_name} onChange={handleChange} required style={styles.input} />
          </div>
          <div style={{ ...styles.field, flex: 1 }}>
            <label style={styles.label}>Last Name</label>
            <input name="last_name" value={form.last_name} onChange={handleChange} required style={styles.input} />
          </div>
        </div>
        <div style={styles.field}>
          <label style={styles.label}>Email</label>
          <input name="email" type="email" value={form.email} onChange={handleChange} required style={styles.input} />
        </div>
        <div style={styles.field}>
          <label style={styles.label}>Password</label>
          <input name="password" type="password" value={form.password} onChange={handleChange} required minLength={8} style={styles.input} />
        </div>
        {error && <p style={{ color: '#e53e3e' }}>{error}</p>}
        <button type="submit" disabled={loading} style={styles.btn}>
          {loading ? 'Creating...' : 'Register'}
        </button>
        <p style={styles.link}>
          Already have an account? <Link to="/login" style={{ color: '#3182ce' }}>Login</Link>
        </p>
      </form>
    </div>
  );
};

const styles: Record<string, React.CSSProperties> = {
  container: { maxWidth: 400, margin: '40px auto' },
  title: { fontSize: 28, marginBottom: 20, textAlign: 'center' },
  form: {
    background: '#fff',
    padding: 24,
    borderRadius: 8,
    border: '1px solid #e2e8f0',
  },
  field: { marginBottom: 16 },
  label: { display: 'block', fontSize: 13, fontWeight: 600, marginBottom: 4, color: '#4a5568' },
  input: {
    width: '100%',
    padding: '10px 12px',
    border: '1px solid #e2e8f0',
    borderRadius: 6,
    fontSize: 14,
    boxSizing: 'border-box',
  },
  btn: {
    width: '100%',
    padding: '12px',
    background: '#3182ce',
    color: '#fff',
    border: 'none',
    borderRadius: 6,
    fontWeight: 'bold',
    fontSize: 16,
    cursor: 'pointer',
  },
  link: { textAlign: 'center', marginTop: 16, fontSize: 14 },
};

export default Register;
