import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { register } from '../../api/auth';
import Input from '../../components/Input/Input';
import Button from '../../components/Button/Button';
import styles from './RegisterPage.module.css';

export default function RegisterPage() {
  const navigate = useNavigate();
  const { login: authLogin } = useAuth();
  
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    password_confirm: '',
    phone_number: '',
    first_name: '',
    last_name: ''
  });
  
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const validateForm = () => {
    if (formData.password !== formData.password_confirm) {
      setError('Пароли не совпадают');
      return false;
    }
    if (formData.password.length < 6) {
      setError('Пароль должен быть не менее 6 символов');
      return false;
    }
    if (!formData.phone_number) {
      setError('Телефон обязателен');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!validateForm()) return;

    setIsLoading(true);
    try {
      const data = await register(formData);
      
      if (data.access) {
        // Автоматический вход после регистрации
        authLogin(data.access, data.user);
        setSuccess('Регистрация успешна! Выполняется вход...');
        setTimeout(() => {
          navigate('/cars');
        }, 1500);
      } else {
        setError('Ошибка при регистрации');
      }
    } catch (err) {
      setError(err.message || 'Ошибка соединения с сервером');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.card}>
        <h2 className={styles.title}>Регистрация в CRM</h2>
        
        <form onSubmit={handleSubmit} className={styles.form}>
          <Input
            type="email"
            name="email"
            label="Email *"
            value={formData.email}
            onChange={handleChange}
            placeholder="Введите email"
            required
          />

          <div className={styles.formRow}>
            <Input
              type="text"
              name="first_name"
              label="Имя"
              value={formData.first_name}
              onChange={handleChange}
              placeholder="Имя"
            />
            <Input
              type="text"
              name="last_name"
              label="Фамилия"
              value={formData.last_name}
              onChange={handleChange}
              placeholder="Фамилия"
            />
          </div>

          <Input
            type="tel"
            name="phone_number"
            label="Телефон *"
            value={formData.phone_number}
            onChange={handleChange}
            placeholder="+7 (999) 123-45-67"
            required
          />

          <Input
            type="password"
            name="password"
            label="Пароль *"
            value={formData.password}
            onChange={handleChange}
            placeholder="Минимум 6 символов"
            required
          />

          <Input
            type="password"
            name="password_confirm"
            label="Подтверждение пароля *"
            value={formData.password_confirm}
            onChange={handleChange}
            placeholder="Повторите пароль"
            required
          />

          <div className={styles.passwordHint}>
            Пароль должен содержать минимум 6 символов
          </div>

          {error && <div className={styles.error}>{error}</div>}
          {success && <div className={styles.success}>{success}</div>}

          <Button
            type="submit"
            disabled={isLoading}
            fullWidth
          >
            {isLoading ? 'Регистрация...' : 'Зарегистрироваться'}
          </Button>
        </form>

        <div className={styles.footer}>
          Уже есть аккаунт?{' '}
          <span 
            className={styles.link}
            onClick={() => navigate('/login')}
          >
            Войти
          </span>
        </div>
      </div>
    </div>
  );
}