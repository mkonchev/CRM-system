import styles from './Input.module.css';

export default function Input({
  type = 'text',
  name,
  label,
  value,
  onChange,
  placeholder,
  required = false,
  error
}) {
  return (
    <div className={styles.container}>
      {label && <label className={styles.label} htmlFor={name}>{label}</label>}
      <input
        id={name}
        type={type}
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        className={`${styles.input} ${error ? styles.error : ''}`}
      />
    </div>
  );
}