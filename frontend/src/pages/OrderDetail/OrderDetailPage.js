import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { fetchOrderById, updateWorkStatus } from '../../api/orders';
import { fetchWorks } from '../../api/works';
import InfoCard from '../../components/InfoCard/InfoCard';
import OrderWorkItem from '../../components/OrderWorkItem/OrderWorkItem';
import OrderChat from '../../components/OrderChat/OrderChat';
import styles from './OrderDetailPage.module.css';

export default function OrderDetailPage() {
  const { id } = useParams();
  const { token, user } = useAuth();
  const [order, setOrder] = useState(null);
  const [works, setWorks] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const canEdit = user?.role === 0 || user?.role === 1;

  useEffect(() => {
    const loadData = async () => {
      try {
        const orderData = await fetchOrderById(token, id);
        setOrder(orderData);

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

  if (loading) return <div className={styles.loading}>Загрузка...</div>;
  if (error) return <div className={styles.error}>Ошибка: {error}</div>;
  if (!order) return <div className={styles.error}>Заказ не найден</div>;

  const car = order.car_details;
  const owner = order.owner_details;
  const worker = order.worker_details;

  return (
    <div className={styles.container}>
      <Link to="/orders" className={styles.backLink}>
        ← Назад к списку
      </Link>

      <h1 className={styles.title}>Заказ #{order.id}</h1>

      <div className={styles.grid}>
        <InfoCard title="👤 Клиент">
          {owner ? (
            <>
              <div className={styles.infoRow}>
                <span className={styles.infoLabel}>Email:</span> {owner.email}
              </div>
              <div className={styles.infoRow}>
                <span className={styles.infoLabel}>Телефон:</span> {owner.phone_number || '—'}
              </div>
              <div className={styles.infoRow}>
                <span className={styles.infoLabel}>Имя:</span> {owner.full_name || owner.email}
              </div>
            </>
          ) : (
            <p>Нет информации</p>
          )}
        </InfoCard>

        <InfoCard title="🔧 Работник">
          {worker ? (
            <>
              <div className={styles.infoRow}>
                <span className={styles.infoLabel}>Email:</span> {worker.email}
              </div>
              <div className={styles.infoRow}>
                <span className={styles.infoLabel}>Телефон:</span> {worker.phone_number || '—'}
              </div>
              <div className={styles.infoRow}>
                <span className={styles.infoLabel}>Имя:</span> {worker.full_name || worker.email}
              </div>
            </>
          ) : (
            <p>Не назначен</p>
          )}
        </InfoCard>

        <InfoCard title="🚗 Машина">
          {car ? (
            <>
              <div className={styles.infoRow}>
                {car.mark} {car.model} ({car.year || '—'})
              </div>
              <div className={styles.infoRow}>
                <span className={styles.infoLabel}>Номер:</span> {car.number || '—'}
              </div>
              <div className={styles.infoRow}>
                <span className={styles.infoLabel}>VIN:</span> {car.vin || '—'}
              </div>
            </>
          ) : (
            <p>Нет информации</p>
          )}
        </InfoCard>

        <InfoCard title="📋 Работы">
          {!order.items || order.items.length === 0 ? (
            <p>Нет работ</p>
          ) : (
            <div className={styles.worksList}>
              {order.items.map(item => (
                <OrderWorkItem
                  key={item.id}
                  item={item}
                  work={works[item.work]}
                  canEdit={canEdit}
                  onStatusChange={handleStatusChange}
                />
              ))}
            </div>
          )}
        </InfoCard>

        <div className={`${styles.orderStatus} ${order.is_completed ? styles.completed : styles.inProgress}`}>
          {order.is_completed ? '✅ Заказ завершён' : '⏳ Заказ в работе'}
        </div>
        <div className={styles.chatSection}>
          <OrderChat orderId={order.id} />
        </div>
      </div>
    </div>
  );
}