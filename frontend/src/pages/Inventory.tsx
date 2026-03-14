import React, { useEffect, useState } from 'react';
import { getInventory, getLowStock, updateStock } from '../api';
import type { InventoryItem } from '../types';

const Inventory: React.FC = () => {
  const [items, setItems] = useState<InventoryItem[]>([]);
  const [showLowOnly, setShowLowOnly] = useState(false);
  const [loading, setLoading] = useState(true);
  const [editId, setEditId] = useState<string | null>(null);
  const [editStock, setEditStock] = useState(0);

  const loadData = async () => {
    setLoading(true);
    try {
      const res = showLowOnly ? await getLowStock() : await getInventory();
      setItems(res.data.results);
    } catch {
      setItems([]);
    }
    setLoading(false);
  };

  useEffect(() => {
    loadData();
  }, [showLowOnly]);

  const handleSave = async (id: string) => {
    await updateStock(id, editStock);
    setEditId(null);
    loadData();
  };

  if (loading) return <p>Loading inventory...</p>;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
        <h1 style={{ fontSize: 28, margin: 0 }}>Inventory Management</h1>
        <label style={{ display: 'flex', alignItems: 'center', gap: 8, cursor: 'pointer' }}>
          <input
            type="checkbox"
            checked={showLowOnly}
            onChange={(e) => setShowLowOnly(e.target.checked)}
          />
          Show low stock only
        </label>
      </div>

      <table style={styles.table}>
        <thead>
          <tr>
            <th style={styles.th}>Product</th>
            <th style={styles.th}>Category</th>
            <th style={styles.th}>Stock</th>
            <th style={styles.th}>Status</th>
            <th style={styles.th}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.id}>
              <td style={styles.td}>{item.title}</td>
              <td style={styles.td}>{item.category_name}</td>
              <td style={styles.td}>
                {editId === item.id ? (
                  <input
                    type="number"
                    min={0}
                    value={editStock}
                    onChange={(e) => setEditStock(parseInt(e.target.value) || 0)}
                    style={{ width: 80, padding: '4px 8px', borderRadius: 4, border: '1px solid #e2e8f0' }}
                  />
                ) : (
                  item.stock
                )}
              </td>
              <td style={styles.td}>
                <span
                  style={{
                    fontSize: 12,
                    padding: '2px 8px',
                    borderRadius: 12,
                    background: item.stock <= 10 ? '#fed7d7' : '#c6f6d5',
                    color: item.stock <= 10 ? '#c53030' : '#276749',
                  }}
                >
                  {item.stock <= 10 ? 'Low Stock' : 'In Stock'}
                </span>
              </td>
              <td style={styles.td}>
                {editId === item.id ? (
                  <div style={{ display: 'flex', gap: 8 }}>
                    <button onClick={() => handleSave(item.id)} style={styles.saveBtn}>Save</button>
                    <button onClick={() => setEditId(null)} style={styles.cancelBtn}>Cancel</button>
                  </div>
                ) : (
                  <button
                    onClick={() => { setEditId(item.id); setEditStock(item.stock); }}
                    style={styles.editBtn}
                  >
                    Edit
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

const styles: Record<string, React.CSSProperties> = {
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    background: '#fff',
    borderRadius: 8,
    overflow: 'hidden',
    border: '1px solid #e2e8f0',
  },
  th: {
    textAlign: 'left',
    padding: '12px 16px',
    background: '#f7fafc',
    borderBottom: '1px solid #e2e8f0',
    fontSize: 13,
    fontWeight: 600,
    color: '#4a5568',
  },
  td: {
    padding: '12px 16px',
    borderBottom: '1px solid #f0f0f0',
    fontSize: 14,
  },
  editBtn: {
    padding: '4px 12px',
    border: '1px solid #3182ce',
    color: '#3182ce',
    background: 'transparent',
    borderRadius: 4,
    cursor: 'pointer',
    fontSize: 13,
  },
  saveBtn: {
    padding: '4px 12px',
    background: '#38a169',
    color: '#fff',
    border: 'none',
    borderRadius: 4,
    cursor: 'pointer',
    fontSize: 13,
  },
  cancelBtn: {
    padding: '4px 12px',
    border: '1px solid #e2e8f0',
    background: '#fff',
    borderRadius: 4,
    cursor: 'pointer',
    fontSize: 13,
  },
};

export default Inventory;
