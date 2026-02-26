import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { fetchOrderById, updateWorkStatus } from '../../api/orders';
import { fetchCarById } from '../../api/cars';
import { fetchUserById } from '../../api/users';
import { fetchWorks } from '../../api/works';

// Статусы работ (должны совпадать с бэкендом)
const STATUSES = {
  0: { label: 'Не начата', color: '#6c757d' },
  1: { label: 'В работе', color: '#ffc107' },
  2: { label: 'Готово', color: '#28a745' }
};

export default function OrderDetailPage() {
  const { id } = useParams();
  const { token, user } = useAuth();
  const [order, setOrder] = useState(null);
  const [car, setCar] = useState(null);
  const [owner, setOwner] = useState(null);
  const [worker, setWorker] = useState(null);
  const [works, setWorks] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const canEdit = user?.role === 0 || user?.role === 1; // admin или worker

  useEffect(() => {
    const loadData = async () => {
      try {
        // Загружаем заказ
        const orderData = await fetchOrderById(token, id);
        console.log('📦 orderData:', orderData);  // ← посмотри в консоль браузера
        setOrder(orderData);

        // Загружаем машину
        if (orderData.car) {
          const carData = await fetchCarById(token, orderData.car);
          setCar(carData);
        }

        // Загружаем владельца
        if (orderData.owner) {
          const ownerData = await fetchUserById(token, orderData.owner);
          setOwner(ownerData);
        }

        // Загружаем работника
        if (orderData.worker) {
          const workerData = await fetchUserById(token, orderData.worker);
          setWorker(workerData);
        }

        // Загружаем все работы (чтобы получить названия)
        const worksData = await fetchWorks(token);
        const worksMap = {};
        worksData.forEach(w => worksMap[w.id] = w);
        setWorks(worksMap);

        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    loadData();
  }, [token, id]);

    const handleStatusChange = async (workstatusId, newStatus) => {
      try {
        await updateWorkStatus(token, workstatusId, newStatus);
        
        // Обновляем локальное состояние
        setOrder(prev => ({
          ...prev,
          items: prev.items.map(item =>
            item.id === workstatusId ? { ...item, status: newStatus } : item
          )
        }));
      } catch (err) {
        alert('Ошибка при обновлении статуса: ' + err.message);
      }
    };

  if (loading) return <div>Загрузка...</div>;
  if (error) return <div style={{ color: 'red' }}>Ошибка: {error}</div>;
  if (!order) return <div>Заказ не найден</div>;

  return (
    <div>
      <Link to="/orders" style={{ display: 'inline-block', marginBottom: '20px' }}>
        ← Назад к списку
      </Link>

      <h1>Заказ #{order.id}</h1>

      <div style={{ display: 'grid', gap: '20px' }}>
        {/* Информация о клиенте */}
        <div style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '15px' }}>
          <h3>👤 Клиент</h3>
          {owner ? (
            <div>
              <div>Email: {owner.email}</div>
              <div>Телефон: {owner.phone_number || '—'}</div>
              <div>Имя: {owner.first_name || '—'} {owner.last_name || ''}</div>
            </div>
          ) : (
            <p>Нет информации</p>
          )}
        </div>

        {/* Информация о работнике */}
        <div style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '15px' }}>
          <h3>🔧 Работник</h3>
          {worker ? (
            <div>
              <div>Email: {worker.email}</div>
              <div>Телефон: {worker.phone_number || '—'}</div>
            </div>
          ) : (
            <p>Не назначен</p>
          )}
        </div>

        {/* Информация о машине */}
        <div style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '15px' }}>
          <h3>🚗 Машина</h3>
          {car ? (
            <div>
              <div>{car.mark} {car.model} ({car.year})</div>
              <div>Номер: {car.number || '—'}</div>
              <div>VIN: {car.vin || '—'}</div>
            </div>
          ) : (
            <p>Нет информации</p>
          )}
        </div>

        {/* Работы в заказе */}
        <div style={{ border: '1px solid #ddd', borderRadius: '8px', padding: '15px' }}>
          <h3>📋 Работы</h3>
          {order.items?.length === 0 ? (
            <p>Нет работ</p>
          ) : (
            <div style={{ display: 'grid', gap: '10px' }}>
              {order.items.map(item => {
                const work = works[item.work];
                const status = STATUSES[item.status] || { label: 'Неизвестно', color: '#aaa' };

                return (
                  <div key={item.id} style={{
                    padding: '10px',
                    border: '1px solid #eee',
                    borderRadius: '5px'
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <div>
                        <strong>{work?.name || 'Неизвестная работа'}</strong>
                        <div style={{ fontSize: '0.9em', color: '#666' }}>
                          {item.amount} × {item.fix_price} ₽ = {item.amount * item.fix_price} ₽
                        </div>
                      </div>
                      
                      {canEdit ? (
                        <select
                          value={item.status}
                          onChange={(e) => handleStatusChange(item.id, parseInt(e.target.value))}
                          style={{
                            padding: '5px',
                            borderRadius: '3px',
                            border: '1px solid #ccc',
                            backgroundColor: status.color,
                            color: 'white',
                            cursor: 'pointer'
                          }}
                        >
                          {Object.entries(STATUSES).map(([value, s]) => (
                            <option key={value} value={value} style={{ backgroundColor: 'white', color: 'black' }}>
                              {s.label}
                            </option>
                          ))}
                        </select>
                      ) : (
                        <span style={{
                          padding: '5px 10px',
                          borderRadius: '3px',
                          backgroundColor: status.color,
                          color: 'white'
                        }}>
                          {status.label}
                        </span>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Статус заказа */}
        <div style={{
          padding: '15px',
          background: order.is_completed ? '#d4edda' : '#fff3cd',
          borderRadius: '8px',
          textAlign: 'center',
          fontWeight: 'bold'
        }}>
          {order.is_completed ? '✅ Заказ завершён' : '⏳ Заказ в работе'}
        </div>
      </div>
    </div>
  );
}