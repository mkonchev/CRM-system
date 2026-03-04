import { useEffect, useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { fetchWorks } from '../../api/works';
import { fetchCarById } from '../../api/cars';
import WorkFilter from '../../components/WorkFilter/WorkFilter';
import WorkCard from '../../components/WorkCard/WorkCard';
import styles from './WorksPage.module.css';

export default function WorksPage() {
  const { token } = useAuth();
  const [works, setWorks] = useState([]);
  const [cars, setCars] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [markFilter, setMarkFilter] = useState('');
  const [applyingFilter, setApplyingFilter] = useState(false);

  const loadWorks = async (filters = {}) => {
    setLoading(true);
    try {
      const worksData = await fetchWorks(token, filters);
      setWorks(worksData);
      
      // Загружаем данные машин
      const carIds = [...new Set(worksData
        .filter(w => w.car)
        .map(w => w.car))];
      
      const carsData = {};
      await Promise.all(carIds.map(async (id) => {
        try {
          carsData[id] = await fetchCarById(token, id);
        } catch (err) {
          console.error(`Ошибка загрузки машины ${id}:`, err);
        }
      }));
      setCars(carsData);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleApplyFilter = () => {
    setApplyingFilter(true);
    loadWorks({ mark: markFilter }).finally(() => setApplyingFilter(false));
  };

  const handleResetFilter = () => {
    setMarkFilter('');
    loadWorks({});
  };

  useEffect(() => {
    loadWorks({});
  }, []);

  if (loading && !applyingFilter) return <div className={styles.loading}>Загрузка...</div>;
  if (error) return <div className={styles.error}>Ошибка: {error}</div>;

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Работы и услуги</h1>
      
      <WorkFilter
        markFilter={markFilter}
        onMarkChange={setMarkFilter}
        onApply={handleApplyFilter}
        onReset={handleResetFilter}
        isApplying={applyingFilter}
      />

      {works.length === 0 ? (
        <div className={styles.empty}>
          <p>Нет работ</p>
        </div>
      ) : (
        <ul className={styles.worksList}>
          {works.map(work => (
            <WorkCard
              key={work.id}
              work={work}
              car={cars[work.car]}
            />
          ))}
        </ul>
      )}
    </div>
  );
}