import { useEffect, useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { fetchCars } from '../../api/cars';
import { fetchWorks, createWork } from '../../api/works';
import { createOrder } from '../../api/orders';
import { fetchWorkers } from '../../api/users';

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
  const [newWorkCarId, setNewWorkCarId] = useState('');
  const [workers, setWorkers] = useState([]);
  const [selectedWorker, setSelectedWorker] = useState('');

  useEffect(() => {
    Promise.all([
      fetchCars(token),
      fetchWorks(token),
      fetchWorkers(token)
    ])
      .then(([carsData, worksData, workersData]) => {
        setCars(carsData);
        setWorks(worksData);
        setWorkers(workersData);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [token]);

  const handleCreateWork = async (e) => {
    e.preventDefault();
    if (!newWorkName || !newWorkPrice) {
      alert('Название и цена обязательны');
      return;
    }

    try {
      const workData = {
        name: newWorkName,
        price: parseInt(newWorkPrice),
        description: newWorkDescription || undefined,
        car: newWorkCarId ? parseInt(newWorkCarId) : null  // ← здесь выбираем машину
      };

      const newWork = await createWork(token, workData);
      
      // Обновляем список работ
      setWorks(prev => [...prev, newWork]);
      
      // Автоматически выбираем созданную работу с количеством 1
      setSelectedWorks(prev => ({
        ...prev,
        [newWork.id]: 1
      }));

      // Сбрасываем форму
      setShowNewWorkForm(false);
      setNewWorkName('');
      setNewWorkPrice('');
      setNewWorkDescription('');
      setNewWorkCarId('');  // ← сбрасываем
    } catch (err) {
      alert('Ошибка при создании работы: ' + err.message);
    }
  };

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
    if (!selectedWorker) {
      alert('Выберите работника');
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
        worker: parseInt(selectedWorker)
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
      setSelectedWorker('');
      setSelectedWorks({});
    } catch (err) {
      alert(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const getWorkDisplayName = (work) => {
    if (!work.car) return work.name;
    
    const car = cars.find(c => c.id === work.car);
    if (car) {
      return `${work.name} (${car.mark} ${car.model} ${car.year})`;
    }
    return `${work.name} (для машины ID: ${work.car})`;
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

        {/* Выбор работника */}
        <div style={{ marginBottom: '20px' }}>
          <h3>Выберите работника</h3>
          <select
            value={selectedWorker}
            onChange={(e) => setSelectedWorker(e.target.value)}
            style={{ width: '100%', padding: '8px' }}
            required
          >
            <option value="">-- Выберите работника --</option>
            {workers.map(worker => (
              <option key={worker.id} value={worker.id}>
                {worker.first_name} {worker.last_name} ({worker.email})
              </option>
            ))}
          </select>
          {workers.length === 0 && (
            <p style={{ color: 'orange' }}>⚠️ Нет доступных работников</p>
          )}
        </div>

        {/* Выбор работ */}
        <div style={{ marginBottom: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h3>Выберите работы</h3>
            <button
              type="button"
              onClick={() => setShowNewWorkForm(true)}
              style={{
                padding: '5px 10px',
                background: '#28a745',
                color: 'white',
                border: 'none',
                borderRadius: '3px',
                cursor: 'pointer'
              }}
            >
              ➕ Новая работа
            </button>
          </div>

          {/* Форма создания новой работы */}
          {showNewWorkForm && (
            <div style={{
              marginBottom: '20px',
              padding: '15px',
              border: '2px solid #28a745',
              borderRadius: '5px',
              background: '#f9fff9'
            }}>
              <h4>Создание новой работы</h4>
              <div style={{ display: 'grid', gap: '10px' }}>
                <input
                  type="text"
                  placeholder="Название работы *"
                  value={newWorkName}
                  onChange={(e) => setNewWorkName(e.target.value)}
                  style={{ padding: '8px' }}
                />
                <input
                  type="number"
                  placeholder="Цена *"
                  value={newWorkPrice}
                  onChange={(e) => setNewWorkPrice(e.target.value)}
                  style={{ padding: '8px' }}
                />
                <textarea
                  placeholder="Описание (необязательно)"
                  value={newWorkDescription}
                  onChange={(e) => setNewWorkDescription(e.target.value)}
                  style={{ padding: '8px' }}
                />
                
                {/* Выбор машины (необязательно) */}
                <div>
                  <label style={{ display: 'block', marginBottom: '5px' }}>
                    Привязать к машине (необязательно):
                  </label>
                  <select
                    value={newWorkCarId}
                    onChange={(e) => setNewWorkCarId(e.target.value)}
                    style={{ width: '100%', padding: '8px' }}
                  >
                    <option value="">-- Нет привязки (общая работа) --</option>
                    {cars.map(car => (
                      <option key={car.id} value={car.id}>
                        {car.mark} {car.model} ({car.year}) - {car.number || 'без номера'}
                      </option>
                    ))}
                  </select>
                </div>

                <div style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
                  <button
                    type="button"
                    onClick={handleCreateWork}
                    style={{
                      padding: '8px 15px',
                      background: '#28a745',
                      color: 'white',
                      border: 'none',
                      borderRadius: '3px',
                      cursor: 'pointer'
                    }}
                  >
                    Создать
                  </button>
                  <button
                    type="button"
                    onClick={() => setShowNewWorkForm(false)}
                    style={{
                      padding: '8px 15px',
                      background: '#6c757d',
                      color: 'white',
                      border: 'none',
                      borderRadius: '3px',
                      cursor: 'pointer'
                    }}
                  >
                    Отмена
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Список работ */}
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
                    <strong>{getWorkDisplayName(work)}</strong> — {work.price} ₽
                    {work.description && <div style={{ color: '#666', fontSize: '0.9em' }}>{work.description}</div>}
                  </div>
                  
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
          disabled={submitting || !selectedCar || !selectedWorker || Object.keys(selectedWorks).length === 0}
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