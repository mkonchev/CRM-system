import styles from './Input.module.css';

export default function Input({
  type = 'text',
  label,
  value,
  onChange,
  placeholder,
  required = false,
  error
}) {
  return (
    <div className={styles.container}>
      {label && <label className={styles.label}>{label}</label>}
      <input
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        className={`${styles.input} ${error ? styles.error : ''}`}
      />
    </div>
  );
}