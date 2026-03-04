import styles from './Button.module.css';

export default function Button({
  children,
  type = 'button',
  onClick,
  disabled = false,
  variant = 'primary',
  fullWidth = false
}) {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`
        ${styles.button} 
        ${styles[variant]} 
        ${fullWidth ? styles.fullWidth : ''}
      `}
    >
      {children}
    </button>
  );
}