import { useEffect, useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { fetchWorks } from '../../api/works';
import { fetchCarById } from '../../api/cars';

export default function WorksPage() {
  const { token } = useAuth();
  const [works, setWorks] = useState([]);
  const [cars, setCars] = useState({}); // кэш машин по ID
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [markFilter, setMarkFilter] = useState('');
  const [applyingFilter, setApplyingFilter] = useState(false);

  const loadWorks = async (filters = {}) => {
    setLoading(true);
    try {
      const worksData = await fetchWorks(token, filters);
      setWorks(worksData);
      
      // Загружаем данные машин для работ, у которых есть car
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

  if (loading && !applyingFilter) return <div>Загрузка...</div>;
  if (error) return <div style={{ color: 'red' }}>Ошибка: {error}</div>;

  return (
    <div>
      <h1>Работы и услуги</h1>
      
      {/* Фильтр по марке машины */}
      <div style={{ marginBottom: '20px', padding: '15px', background: '#f5f5f5', borderRadius: '5px' }}>
        <h3>Фильтр по машине</h3>
        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          <input
            type="text"
            placeholder="Марка машины (например, Toyota)"
            value={markFilter}
            onChange={(e) => setMarkFilter(e.target.value)}
            style={{ padding: '8px', flex: 1 }}
          />
          <button 
            onClick={handleApplyFilter}
            disabled={applyingFilter}
            style={{ padding: '8px 15px', background: '#007bff', color: 'white', border: 'none', borderRadius: '3px', cursor: 'pointer' }}
          >
            {applyingFilter ? 'Поиск...' : 'Применить'}
          </button>
          <button 
            onClick={handleResetFilter}
            style={{ padding: '8px 15px', background: '#6c757d', color: 'white', border: 'none', borderRadius: '3px', cursor: 'pointer' }}
          >
            Сбросить
          </button>
        </div>
      </div>

      {works.length === 0 ? (
        <p>Нет работ</p>
      ) : (
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {works.map(work => (
            <li key={work.id} style={{
              border: '1px solid #ccc',
              margin: '10px 0',
              padding: '15px',
              borderRadius: '5px'
            }}>
              <div><strong>{work.name}</strong></div>
              {work.description && <div style={{ color: '#666', marginTop: '5px' }}>{work.description}</div>}
              <div style={{ marginTop: '5px' }}>Цена: <strong>{work.price} ₽</strong></div>
              
              {/* Информация о машине, если работа привязана */}
              {work.car && cars[work.car] && (
                <div style={{ 
                  marginTop: '10px', 
                  padding: '8px', 
                  background: '#e9f7fe', 
                  borderRadius: '3px',
                  fontSize: '0.9em'
                }}>
                  <span style={{ fontWeight: 'bold' }}>Для машины:</span>{' '}
                  {cars[work.car].mark} {cars[work.car].model} ({cars[work.car].year})
                </div>
              )}
              
              {/* Если работа общая (без машины) */}
              {!work.car && (
                <div style={{ 
                  marginTop: '10px', 
                  padding: '8px', 
                  background: '#f0f0f0', 
                  borderRadius: '3px',
                  fontSize: '0.9em',
                  color: '#666'
                }}>
                  ⚡ Общая работа (для любой машины)
                </div>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}