import { useEffect, useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { fetchGroupedWorks } from '../../api/works';
import styles from './WorksPage.module.css';

export default function WorksPage() {
  const { token } = useAuth();
  const [works, setWorks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchGroupedWorks(token)
      .then(data => {
        setWorks(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [token]);

  if (loading) return <div className={styles.loading}>Загрузка...</div>;
  if (error) return <div className={styles.error}>Ошибка: {error}</div>;

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Работы и услуги</h1>

      {works.length === 0 ? (
        <div className={styles.empty}>Нет работ</div>
      ) : (
        <ul className={styles.worksList}>
          {works.map((work, idx) => (
            <li key={idx} className={styles.workCard}>
              <div className={styles.workHeader}>
                <span className={styles.workName}>{work.name}</span>
                <span className={styles.workPrice}>{work.price_range}</span>
              </div>
              <div className={styles.workStats}>
                <span>💰 Мин. цена: {work.min_price} ₽</span>
                <span>📈 Макс. цена: {work.max_price} ₽</span>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}