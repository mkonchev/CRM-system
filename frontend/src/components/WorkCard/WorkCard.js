import styles from './WorkCard.module.css';

export default function WorkCard({ work, car }) {
  return (
    <li className={styles.card}>
      <div className={styles.header}>
        <h3 className={styles.title}>{work.name}</h3>
        <span className={styles.price}>{work.price} ₽</span>
      </div>
      
      {work.description && (
        <div className={styles.description}>{work.description}</div>
      )}
      
      {work.car && car ? (
        <div className={styles.carInfo}>
          <span className={styles.carLabel}>Для машины:</span>
          <span className={styles.carDetails}>
            {car.mark} {car.model} ({car.year})
          </span>
        </div>
      ) : !work.car && (
        <div className={styles.generalWork}>
          ⚡ Общая работа (для любой машины)
        </div>
      )}
    </li>
  );
}