import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { fetchUsers } from '../api/users';
import styles from './CarForm.module.css';

export default function CarForm({ onCarCreated }) {
  const { token, user } = useAuth();
  const [mark, setMark] = useState('');
  const [model, setModel] = useState('');
  const [year, setYear] = useState('');
  const [number, setNumber] = useState('');
  const [vin, setVin] = useState('');
  const [ownerId, setOwnerId] = useState('');
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);

  const isAdminOrWorker = user?.role === 0 || user?.role === 1;

  useEffect(() => {
    if (isAdminOrWorker && token) {
      fetchUsers(token).then(setUsers).catch(console.error);
    }
  }, [isAdminOrWorker, token]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const carData = {
        mark,
        model,
        year: year ? Number(year) : null,
        number,
        vin: vin || null
      };
      if (isAdminOrWorker && ownerId) {
        carData.owner = parseInt(ownerId);
      }
      
      await onCarCreated(carData);
      setMark('');
      setModel('');
      setYear('');
      setNumber('');
      setVin('');
      setOwnerId('');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className={styles.form}>
      <h3>Добавить машину</h3>
      <div className={styles.formGroup}>
        <input
          placeholder="Марка (можно не заполнять, если есть VIN)"
          value={mark}
          onChange={(e) => setMark(e.target.value)}
          className={styles.input}
        />
        <input
          placeholder="Модель (можно не заполнять, если есть VIN)"
          value={model}
          onChange={(e) => setModel(e.target.value)}
          className={styles.input}
        />
        <input
          placeholder="Год (можно не заполнять, если есть VIN)"
          type="number"
          value={year}
          onChange={(e) => setYear(e.target.value)}
          className={styles.input}
        />
        <input
          placeholder="Госномер"
          value={number}
          onChange={(e) => setNumber(e.target.value)}
          className={styles.input}
        />
        <input
          placeholder="VIN (если ввести, марка/модель/год заполнятся автоматически)"
          value={vin}
          onChange={(e) => setVin(e.target.value)}
          className={styles.input}
        />
        {isAdminOrWorker && users.length > 0 && (
          <select
            value={ownerId}
            onChange={(e) => setOwnerId(e.target.value)}
            className={styles.select}
          >
            <option value="">-- Выберите владельца --</option>
            {users.map(u => (
              <option key={u.id} value={u.id}>
                {u.email} {u.first_name ? `(${u.first_name} ${u.last_name})` : ''}
              </option>
            ))}
          </select>
        )}
        
        <button type="submit" disabled={loading} className={styles.button}>
          {loading ? 'Сохранение...' : 'Добавить'}
        </button>
      </div>
    </form>
  );
}