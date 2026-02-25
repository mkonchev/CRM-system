import { useEffect, useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { fetchCars } from '../../api/cars';
import { fetchWorks } from '../../api/works';
import { createOrder } from '../../api/orders';

export default function CreateOrderPage() {
  const { token } = useAuth();
  const [cars, setCars] = useState([]);
  const [works, setWorks] = useState([]);
  const [selectedCar, setSelectedCar] = useState('');
  const [selectedWorks, setSelectedWorks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    Promise.all([
      fetchCars(token),
      fetchWorks(token)
    ])
      .then(([carsData, worksData]) => {
        setCars(carsData);
        setWorks(worksData);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [token]);

  const handleWorkToggle = (workId) => {
    setSelectedWorks(prev =>
      prev.includes(workId)
        ? prev.filter(id => id !== workId)
        : [...prev, workId]
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedCar) {
      alert('Выберите машину');
      return;
    }
    if (selectedWorks.length === 0) {
      alert('Выберите хотя бы одну работу');
      return;
    }

    setSubmitting(true);
    try {
      // Создаём заказ
      const order = await createOrder(token, {
        car: parseInt(selectedCar),
        // owner и worker пока не передаём — бэкенд сам подставит
      });

      // Добавляем работы в заказ (Workstatus)
      await Promise.all(selectedWorks.map(async (workId) => {
        const response = await fetch('/api/workstatus/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            order: order.id,
            work: workId,
            amount: 1,
            status: 0
          })
        });
        
        const data = await response.json();
        console.log('Ответ сервера:', data); // ← смотрим, что в ответе
        
        if (!response.ok) {
          throw new Error(JSON.stringify(data));
        }
      }));

      alert('Заказ создан!');
      // Очищаем форму
      setSelectedCar('');
      setSelectedWorks([]);
    } catch (err) {
      alert(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <div>Загрузка...</div>;
  if (error) return <div style={{ color: 'red' }}>Ошибка: {error}</div>;

  const totalPrice = selectedWorks.reduce((sum, workId) => {
    const work = works.find(w => w.id === workId);
    return sum + (work?.price || 0);
  }, 0);

  return (
    <div>
      <h1>Создание заказа</h1>
      
      <form onSubmit={handleSubmit}>
        {/* Выбор машины */}
        <div style={{ marginBottom: '20px' }}>
          <h3>Выберите машину</h3>
          <select
            value={selectedCar}
            onChange={(e) => setSelectedCar(e.target.value)}
            style={{ width: '100%', padding: '8px' }}
          >
            <option value="">-- Выберите машину --</option>
            {cars.map(car => (
              <option key={car.id} value={car.id}>
                {car.mark} {car.model} ({car.year}) - {car.number || 'без номера'}
              </option>
            ))}
          </select>
        </div>

        {/* Выбор работ */}
        <div style={{ marginBottom: '20px' }}>
          <h3>Выберите работы</h3>
          <div style={{ display: 'grid', gap: '10px' }}>
            {works.map(work => (
              <label key={work.id} style={{
                display: 'block',
                padding: '10px',
                border: '1px solid #ccc',
                borderRadius: '5px',
                cursor: 'pointer',
                background: selectedWorks.includes(work.id) ? '#e3f2fd' : 'white'
              }}>
                <input
                  type="checkbox"
                  checked={selectedWorks.includes(work.id)}
                  onChange={() => handleWorkToggle(work.id)}
                  style={{ marginRight: '10px' }}
                />
                <strong>{work.name}</strong> — {work.price} ₽
                {work.description && <div style={{ color: '#666', fontSize: '0.9em' }}>{work.description}</div>}
              </label>
            ))}
          </div>
        </div>

        {/* Итого */}
        {selectedWorks.length > 0 && (
          <div style={{
            padding: '15px',
            background: '#f5f5f5',
            borderRadius: '5px',
            marginBottom: '20px'
          }}>
            <h3>Итого: {totalPrice} ₽</h3>
          </div>
        )}

        {/* Кнопка отправки */}
        <button
          type="submit"
          disabled={submitting || !selectedCar || selectedWorks.length === 0}
          style={{
            padding: '10px 20px',
            background: '#28a745',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
            fontSize: '16px'
          }}
        >
          {submitting ? 'Создание...' : 'Создать заказ'}
        </button>
      </form>
    </div>
  );
}