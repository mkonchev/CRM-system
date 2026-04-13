import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { fetchOrders } from '../../api/orders';
import OrderCard from '../../components/OrderCard/OrderCard';
import styles from './OrdersPage.module.css';

export default function OrdersPage() {
  const { token, user } = useAuth();
  const [orders, setOrders] = useState([]);
  const [filteredOrders, setFilteredOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const canCreateOrder = user?.role === 0 || user?.role === 1;

  useEffect(() => {
    fetchOrders(token)
      .then(ordersData => {
        const ordersArray = Array.isArray(ordersData) ? ordersData : ordersData.results || [];
        setOrders(ordersArray);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [token]);

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
              car={order.car_details}
              owner={order.owner_details}
              worker={order.worker_details}
            />
          ))}
        </div>
      )}
    </div>
  );
}