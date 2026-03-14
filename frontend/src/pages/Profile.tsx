import React, { useEffect, useState } from 'react';
import { useAuth } from '../store/AuthContext';
import { getDistrictProfile, updateProfile, updateDistrictProfile } from '../api';
import type { DistrictProfile } from '../types';

const Profile: React.FC = () => {
  const { user, refreshUser } = useAuth();
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [district, setDistrict] = useState<DistrictProfile | null>(null);
  const [districtForm, setDistrictForm] = useState({
    district_name: '',
    state: '',
    student_count: 0,
    ell_percentage: '',
    free_reduced_lunch_pct: '',
    grade_levels_served: '' as string,
  });
  const [msg, setMsg] = useState('');

  useEffect(() => {
    if (user) {
      setFirstName(user.first_name);
      setLastName(user.last_name);
    }
    getDistrictProfile().then((res) => {
      setDistrict(res.data);
      setDistrictForm({
        district_name: res.data.district_name,
        state: res.data.state,
        student_count: res.data.student_count,
        ell_percentage: res.data.ell_percentage,
        free_reduced_lunch_pct: res.data.free_reduced_lunch_pct,
        grade_levels_served: res.data.grade_levels_served.join(', '),
      });
    }).catch(() => {});
  }, [user]);

  const saveProfile = async () => {
    await updateProfile({ first_name: firstName, last_name: lastName });
    await refreshUser();
    setMsg('Profile saved!');
    setTimeout(() => setMsg(''), 2000);
  };

  const saveDistrict = async () => {
    const data = {
      district_name: districtForm.district_name,
      state: districtForm.state,
      student_count: districtForm.student_count,
      ell_percentage: districtForm.ell_percentage,
      free_reduced_lunch_pct: districtForm.free_reduced_lunch_pct,
      grade_levels_served: districtForm.grade_levels_served.split(',').map((s) => s.trim()).filter(Boolean),
    };
    const res = await updateDistrictProfile(data);
    setDistrict(res.data);
    setMsg('District profile saved!');
    setTimeout(() => setMsg(''), 2000);
  };

  if (!user) return <p>Loading...</p>;

  return (
    <div style={{ maxWidth: 600, margin: '0 auto' }}>
      <h1 style={{ fontSize: 28, marginBottom: 20 }}>Profile</h1>

      {msg && <div style={styles.msg}>{msg}</div>}

      <div style={styles.section}>
        <h3>Personal Information</h3>
        <p style={{ fontSize: 13, color: '#718096' }}>{user.email}</p>
        <div style={{ display: 'flex', gap: 12, marginTop: 12 }}>
          <div style={styles.field}>
            <label style={styles.label}>First Name</label>
            <input value={firstName} onChange={(e) => setFirstName(e.target.value)} style={styles.input} />
          </div>
          <div style={styles.field}>
            <label style={styles.label}>Last Name</label>
            <input value={lastName} onChange={(e) => setLastName(e.target.value)} style={styles.input} />
          </div>
        </div>
        <button onClick={saveProfile} style={styles.btn}>Save Profile</button>
      </div>

      <div style={styles.section}>
        <h3>District Profile</h3>
        <div style={styles.field}>
          <label style={styles.label}>District Name</label>
          <input
            value={districtForm.district_name}
            onChange={(e) => setDistrictForm({ ...districtForm, district_name: e.target.value })}
            style={styles.input}
          />
        </div>
        <div style={{ display: 'flex', gap: 12 }}>
          <div style={{ ...styles.field, flex: 1 }}>
            <label style={styles.label}>State</label>
            <input
              value={districtForm.state}
              onChange={(e) => setDistrictForm({ ...districtForm, state: e.target.value })}
              style={styles.input}
              maxLength={2}
            />
          </div>
          <div style={{ ...styles.field, flex: 1 }}>
            <label style={styles.label}>Student Count</label>
            <input
              type="number"
              value={districtForm.student_count}
              onChange={(e) => setDistrictForm({ ...districtForm, student_count: parseInt(e.target.value) || 0 })}
              style={styles.input}
            />
          </div>
        </div>
        <div style={{ display: 'flex', gap: 12 }}>
          <div style={{ ...styles.field, flex: 1 }}>
            <label style={styles.label}>ELL %</label>
            <input
              value={districtForm.ell_percentage}
              onChange={(e) => setDistrictForm({ ...districtForm, ell_percentage: e.target.value })}
              style={styles.input}
            />
          </div>
          <div style={{ ...styles.field, flex: 1 }}>
            <label style={styles.label}>Free/Reduced Lunch %</label>
            <input
              value={districtForm.free_reduced_lunch_pct}
              onChange={(e) => setDistrictForm({ ...districtForm, free_reduced_lunch_pct: e.target.value })}
              style={styles.input}
            />
          </div>
        </div>
        <div style={styles.field}>
          <label style={styles.label}>Grade Levels Served (comma-separated)</label>
          <input
            value={districtForm.grade_levels_served}
            onChange={(e) => setDistrictForm({ ...districtForm, grade_levels_served: e.target.value })}
            style={styles.input}
            placeholder="K, 1, 2, 3, 4, 5"
          />
        </div>
        <button onClick={saveDistrict} style={styles.btn}>Save District Profile</button>
      </div>
    </div>
  );
};

const styles: Record<string, React.CSSProperties> = {
  section: {
    background: '#fff',
    border: '1px solid #e2e8f0',
    borderRadius: 8,
    padding: 20,
    marginBottom: 20,
  },
  field: { marginBottom: 12, flex: 1 },
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
    padding: '10px 20px',
    background: '#3182ce',
    color: '#fff',
    border: 'none',
    borderRadius: 6,
    fontWeight: 'bold',
    cursor: 'pointer',
    marginTop: 8,
  },
  msg: {
    background: '#c6f6d5',
    color: '#276749',
    padding: '10px 16px',
    borderRadius: 6,
    marginBottom: 16,
    fontSize: 14,
  },
};

export default Profile;
