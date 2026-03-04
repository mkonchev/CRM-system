import styles from './WorkItem.module.css';

export default function WorkItem({
  work,
  isSelected,
  quantity,
  displayName,
  onToggle,
  onQuantityChange
}) {
  return (
    <div className={`${styles.workItem} ${isSelected ? styles.selected : ''}`}>
      <div className={styles.workContent}>
        <input
          type="checkbox"
          checked={isSelected}
          onChange={() => onToggle(work.id)}
          className={styles.checkbox}
        />
        
        <div className={styles.workInfo}>
          <div>
            <span className={styles.workName}>{displayName}</span>
            <span className={styles.workPrice}>{work.price} ₽</span>
          </div>
          {work.description && (
            <div className={styles.workDescription}>{work.description}</div>
          )}
        </div>

        {isSelected && (
          <div className={styles.quantityControls}>
            <button
              type="button"
              onClick={() => onQuantityChange(work.id, quantity - 1)}
              className={styles.quantityButton}
            >-</button>
            <span className={styles.quantity}>{quantity}</span>
            <button
              type="button"
              onClick={() => onQuantityChange(work.id, quantity + 1)}
              className={styles.quantityButton}
            >+</button>
          </div>
        )}
      </div>
    </div>
  );
}