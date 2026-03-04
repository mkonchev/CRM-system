import WorkStatus from '../WorkStatus/WorkStatus';
import styles from './OrderWorkItem.module.css';

export default function OrderWorkItem({ item, work, canEdit, onStatusChange }) {
  const workName = work?.name || 'Неизвестная работа';
  const totalPrice = item.amount * item.fix_price;

  return (
    <div className={styles.item}>
      <div className={styles.header}>
        <div>
          <span className={styles.name}>{workName}</span>
          <span className={styles.price}>{item.fix_price} ₽</span>
        </div>
        <WorkStatus
          status={item.status}
          canEdit={canEdit}
          onChange={(newStatus) => onStatusChange(item.id, newStatus)}
        />
      </div>
      <div className={styles.details}>
        {item.amount} × {item.fix_price} ₽ ={' '}
        <span className={styles.total}>{totalPrice} ₽</span>
      </div>
      {work?.description && (
        <div className={styles.description}>{work.description}</div>
      )}
    </div>
  );
}