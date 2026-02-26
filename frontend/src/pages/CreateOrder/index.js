import { useEffect, useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { fetchCars } from '../../api/cars';
import { fetchWorks, createWork } from '../../api/works';
import { createOrder } from '../../api/orders';

export default function CreateOrderPage() {
  const { token } = useAuth();
  const [cars, setCars] = useState([]);
  const [works, setWorks] = useState([]);
  const [selectedCar, setSelectedCar] = useState('');
  const [selectedWorks, setSelectedWorks] = useState({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [showNewWorkForm, setShowNewWorkForm] = useState(false);
  const [newWorkName, setNewWorkName] = useState('');
  const [newWorkPrice, setNewWorkPrice] = useState('');
  const [newWorkDescription, setNewWorkDescription] = useState('');
  const [newWorkForSelectedCar, setNewWorkForSelectedCar] = useState(false);

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
    setSelectedWorks(prev => {
      const newSelected = { ...prev };
      if (newSelected[workId]) {
        delete newSelected[workId]; // убираем, если уже выбрано
      } else {
        newSelected[workId] = 1; // добавляем с количеством 1
      }
      return newSelected;
    });
  };

  const handleQuantityChange = (workId, newQuantity) => {
    if (newQuantity < 1) {
      // если количество стало 0 — убираем работу
      setSelectedWorks(prev => {
        const newSelected = { ...prev };
        delete newSelected[workId];
        return newSelected;
      });
    } else {
      setSelectedWorks(prev => ({
        ...prev,
        [workId]: newQuantity
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedCar) {
      alert('Выберите машину');
      return;
    }
    if (Object.keys(selectedWorks).length === 0) {
      alert('Выберите хотя бы одну работу');
      return;
    }

    setSubmitting(true);
    try {
      // Создаём заказ
      const order = await createOrder(token, {
        car: parseInt(selectedCar),
      });

      // Добавляем работы в заказ (Workstatus)
      await Promise.all(Object.entries(selectedWorks).map(async ([workId, quantity]) => {
        const response = await fetch('/api/workstatus/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            order: order.id,
            work: parseInt(workId),
            amount: quantity,
            status: 0
          })
        });

        if (!response.ok) {
          const data = await response.json();
          throw new Error(JSON.stringify(data));
        }
      }));

      alert('Заказ создан!');
      // Очищаем форму
      setSelectedCar('');
      setSelectedWorks({});
    } catch (err) {
      alert(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <div>Загрузка...</div>;
  if (error) return <div style={{ color: 'red' }}>Ошибка: {error}</div>;

  const totalPrice = Object.entries(selectedWorks).reduce((sum, [workId, quantity]) => {
    const work = works.find(w => w.id === parseInt(workId));
    return sum + (work?.price || 0) * quantity;
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
              <div key={work.id} style={{
                padding: '10px',
                border: '1px solid #ccc',
                borderRadius: '5px',
                background: selectedWorks[work.id] ? '#e3f2fd' : 'white'
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <input
                    type="checkbox"
                    checked={!!selectedWorks[work.id]}
                    onChange={() => handleWorkToggle(work.id)}
                  />
                  <div style={{ flex: 1 }}>
                    <strong>{work.name}</strong> — {work.price} ₽
                    {work.description && <div style={{ color: '#666', fontSize: '0.9em' }}>{work.description}</div>}
                  </div>
                  
                  {/* Поле для количества */}
                  {selectedWorks[work.id] && (
                    <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
                      <button
                        type="button"
                        onClick={() => handleQuantityChange(work.id, selectedWorks[work.id] - 1)}
                        style={{ width: '30px', height: '30px' }}
                      >-</button>
                      <span style={{ minWidth: '30px', textAlign: 'center' }}>
                        {selectedWorks[work.id]}
                      </span>
                      <button
                        type="button"
                        onClick={() => handleQuantityChange(work.id, selectedWorks[work.id] + 1)}
                        style={{ width: '30px', height: '30px' }}
                      >+</button>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Итого */}
        {Object.keys(selectedWorks).length > 0 && (
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
          disabled={submitting || !selectedCar || Object.keys(selectedWorks).length === 0}
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