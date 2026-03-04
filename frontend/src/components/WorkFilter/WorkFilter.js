import styles from './WorkFilter.module.css';

export default function WorkFilter({
  markFilter,
  onMarkChange,
  onApply,
  onReset,
  isApplying
}) {
  const handleSubmit = (e) => {
    e.preventDefault();
    onApply();
  };

  return (
    <div className={styles.container}>
      <h3 className={styles.title}>Фильтр по машине</h3>
      <form onSubmit={handleSubmit} className={styles.form}>
        <input
          type="text"
          placeholder="Марка машины (например, Toyota)"
          value={markFilter}
          onChange={(e) => onMarkChange(e.target.value)}
          className={styles.input}
        />
        <div className={styles.actions}>
          <button
            type="submit"
            disabled={isApplying}
            className={styles.applyButton}
          >
            {isApplying ? 'Поиск...' : 'Применить'}
          </button>
          <button
            type="button"
            onClick={onReset}
            className={styles.resetButton}
          >
            Сбросить
          </button>
        </div>
      </form>
    </div>
  );
}