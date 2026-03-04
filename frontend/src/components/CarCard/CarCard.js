import styles from './CarCard.module.css';

export default function CarCard({ car, onDelete }) {
  return (
    <li className={styles.card}>
      <div>
        <span className={styles.cardTitle}>
          {car.mark} {car.model} ({car.year})
        </span>
      </div>
      <div className={styles.cardDetail}>Номер: {car.number || '—'}</div>
      <div className={styles.cardDetail}>VIN: {car.vin || '—'}</div>
      <button
        onClick={() => onDelete(car.id)}
        className={styles.deleteButton}
      >
        Удалить
      </button>
    </li>
  );
}