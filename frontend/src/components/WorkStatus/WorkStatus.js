import styles from './WorkStatus.module.css';

const STATUSES = {
  0: { label: 'Не начата', color: '#6c757d' },
  1: { label: 'В работе', color: '#ffc107' },
  2: { label: 'Готово', color: '#28a745' }
};

export default function WorkStatus({ status, canEdit, onChange }) {
  const currentStatus = STATUSES[status] || { label: 'Неизвестно', color: '#aaa' };

  if (canEdit) {
    return (
      <select
        value={status}
        onChange={(e) => onChange(parseInt(e.target.value))}
        className={styles.select}
        style={{ backgroundColor: currentStatus.color }}
      >
        {Object.entries(STATUSES).map(([value, s]) => (
          <option key={value} value={value} style={{ backgroundColor: 'white', color: 'black' }}>
            {s.label}
          </option>
        ))}
      </select>
    );
  }

  return (
    <span
      className={styles.badge}
      style={{ backgroundColor: currentStatus.color }}
    >
      {currentStatus.label}
    </span>
  );
}