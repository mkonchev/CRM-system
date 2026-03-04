import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { fetchOrders } from '../../api/orders';
import { fetchCars } from '../../api/cars';
import { fetchUsers } from '../../api/users';
import OrderCard from '../../components/OrderCard/OrderCard';
import styles from './OrdersPage.module.css';

export default function OrdersPage() {
  const { token, user } = useAuth();
  const [orders, setOrders] = useState([]);
  const [filteredOrders, setFilteredOrders] = useState([]);
  const [cars, setCars] = useState({});
  const [users, setUsers] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const canCreateOrder = user?.role === 0 || user?.role === 1;

  useEffect(() => {
    Promise.all([
      fetchOrders(token),
      fetchCars(token),
      fetchUsers(token)
    ])
      .then(([ordersData, carsData, usersData]) => {
        setOrders(ordersData);

        const carsMap = {};
        carsData.forEach(car => carsMap[car.id] = car);
        setCars(carsMap);

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

  // Фильтруем заказы для воркера
  useEffect(() => {
    if (orders.length > 0 && user) {
      if (user.role === 1) {
        setFilteredOrders(orders.filter(order => order.worker === user.id));
      } else {
        setFilteredOrders(orders);
      }
    }
  }, [orders, user]);

  if (loading) return <div className={styles.loading}>Загрузка...</div>;
  if (error) return <div className={styles.error}>Ошибка: {error}</div>;

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>Заказы</h1>
        {canCreateOrder && (
          <Link to="/create-order" className={styles.createButton}>
            ➕ Создать заказ
          </Link>
        )}
      </div>

      {filteredOrders.length === 0 ? (
        <div className={styles.empty}>
          <p>Нет заказов</p>
        </div>
      ) : (
        <div className={styles.ordersGrid}>
          {filteredOrders.map(order => (
            <OrderCard
              key={order.id}
              order={order}
              car={cars[order.car]}
              owner={users[order.owner]}
              worker={users[order.worker]}
            />
          ))}
        </div>
      )}
    </div>
  );
}