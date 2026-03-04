import { Link } from 'react-router-dom';
import styles from './OrderCard.module.css';

export default function OrderCard({ order, car, owner, worker }) {
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('ru-RU');
  };

  return (
    <Link to={`/orders/${order.id}`} className={styles.link}>
      <div className={styles.card}>
        <div className={styles.content}>
          <div className={styles.info}>
            <div className={styles.title}>Заказ #{order.id}</div>
            
            <div className={styles.details}>
              {car && (
                <div className={styles.detailRow}>
                  <span className={styles.icon}>🚗</span>
                  {car.mark} {car.model} ({car.year})
                </div>
              )}
              
              {owner && (
                <div className={styles.detailRow}>
                  <span className={styles.icon}>👤</span>
                  {owner.email}
                </div>
              )}
              
              {worker && (
                <div className={styles.detailRow}>
                  <span className={styles.icon}>🔧</span>
                  {worker.email}
                </div>
              )}
            </div>
          </div>

          <div className={styles.meta}>
            <div className={styles.date}>
              {formatDate(order.start_date)}
            </div>
            <div className={`${styles.status} ${order.is_completed ? styles.completed : styles.inProgress}`}>
              {order.is_completed ? '✅ Завершён' : '⏳ В работе'}
            </div>
          </div>
        </div>
      </div>
    </Link>
  );
}