import { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { login } from '../../api/auth';
import Input from '../../components/Input/Input';
import Button from '../../components/Button/Button';
import styles from './LoginPage.module.css';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login: authLogin } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const data = await login(email, password);
      if (data.access) {
        authLogin(data.access, data.user);
      } else {
        setError('Неверный email или пароль');
      }
    } catch (err) {
      setError('Ошибка соединения с сервером');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <h2 className={styles.title}>Вход в CRM</h2>
        
        <form onSubmit={handleSubmit} className={styles.form}>
          <Input
            type="email"
            label="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Введите email"
            required
          />

          <Input
            type="password"
            label="Пароль"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Введите пароль"
            required
          />

          {error && <div className={styles.error}>{error}</div>}

          <Button
            type="submit"
            disabled={isLoading}
            fullWidth
          >
            {isLoading ? 'Вход...' : 'Войти'}
          </Button>
        </form>

        <div className={styles.footer}>
          Нет аккаунта?{' '}
          <span className={styles.link}>
            Зарегистрироваться
          </span>
        </div>
      </div>
    </div>
  );
}