import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { fetchOrders } from '../../api/orders';
import { fetchCars } from '../../api/cars';
import { fetchUsers } from '../../api/users';

export default function OrdersPage() {
  const { token, user } = useAuth();
  const [orders, setOrders] = useState([]);
  const [cars, setCars] = useState({});
  const [users, setUsers] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const canCreateOrder = user?.role === 0 || user?.role === 1; // admin или worker

  useEffect(() => {
    Promise.all([
      fetchOrders(token),
      fetchCars(token),
      fetchUsers(token)
    ])
      .then(([ordersData, carsData, usersData]) => {
        setOrders(ordersData);
        
        // Индексируем машины по ID
        const carsMap = {};
        carsData.forEach(car => carsMap[car.id] = car);
        setCars(carsMap);
        
        // Индексируем пользователей по ID
        const usersMap = {};
        usersData.forEach(u => usersMap[u.id] = u);
        setUsers(usersMap);
        
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [token]);

  if (loading) return <div>Загрузка...</div>;
  if (error) return <div style={{ color: 'red' }}>Ошибка: {error}</div>;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Заказы</h1>
        {canCreateOrder && (
          <Link
            to="/create-order"
            style={{
              padding: '10px 20px',
              background: '#28a745',
              color: 'white',
              textDecoration: 'none',
              borderRadius: '5px'
            }}
          >
            ➕ Создать заказ
          </Link>
        )}
      </div>

      {orders.length === 0 ? (
        <p>Нет заказов</p>
      ) : (
        <div style={{ display: 'grid', gap: '15px', marginTop: '20px' }}>
          {orders.map(order => {
            const car = cars[order.car];
            const owner = users[order.owner];
            const worker = users[order.worker];

            return (
              <Link
                key={order.id}
                to={`/orders/${order.id}`}
                style={{
                  textDecoration: 'none',
                  color: 'inherit'
                }}
              >
                <div style={{
                  border: '1px solid #ddd',
                  borderRadius: '8px',
                  padding: '15px',
                  background: '#f9f9f9',
                  cursor: 'pointer'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <div>
                      <strong>Заказ #{order.id}</strong>
                      <div style={{ marginTop: '5px' }}>
                        {car && (
                          <div>🚗 {car.mark} {car.model} ({car.year})</div>
                        )}
                        {owner && (
                          <div>👤 Клиент: {owner.email}</div>
                        )}
                        {worker && (
                          <div>🔧 Работник: {worker.email}</div>
                        )}
                      </div>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <div>📅 {new Date(order.start_date).toLocaleDateString()}</div>
                      <div style={{
                        marginTop: '5px',
                        color: order.is_completed ? '#28a745' : '#ffc107',
                        fontWeight: 'bold'
                      }}>
                        {order.is_completed ? '✅ Завершён' : '⏳ В работе'}
                      </div>
                    </div>
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      )}
    </div>
  );
}