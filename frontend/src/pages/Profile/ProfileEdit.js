import { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { updateUserProfile } from '../../api/users';
import Input from '../../components/Input/Input';
import Button from '../../components/Button/Button';
import styles from './ProfileEdit.module.css';

export default function ProfileEdit() {
  const { token, user, login } = useAuth();
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    phone_number: '',
    tg_login: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    if (user) {
      setFormData({
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        phone_number: user.phone_number || '',
        tg_login: user.tg_login || ''
      });
    }
  }, [user]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const updatedUser = await updateUserProfile(token, user.id, formData);
      
      login(token, updatedUser);
      setSuccess('Профиль успешно обновлён!');
      
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Редактирование профиля</h1>
      
      <form onSubmit={handleSubmit} className={styles.form}>
        <Input
          name="first_name"
          label="Имя"
          value={formData.first_name}
          onChange={handleChange}
          placeholder="Введите имя"
        />
        
        <Input
          name="last_name"
          label="Фамилия"
          value={formData.last_name}
          onChange={handleChange}
          placeholder="Введите фамилию"
        />
        
        <Input
          name="phone_number"
          label="Телефон"
          value={formData.phone_number}
          onChange={handleChange}
          placeholder="+7 (999) 123-45-67"
        />
        
        <Input
          name="tg_login"
          label="Telegram"
          value={formData.tg_login}
          onChange={handleChange}
          placeholder="@username"
        />
        
        {error && <div className={styles.error}>{error}</div>}
        {success && <div className={styles.success}>{success}</div>}
        
        <div className={styles.actions}>
          <Button type="submit" disabled={loading}>
            {loading ? 'Сохранение...' : 'Сохранить'}
          </Button>
        </div>
      </form>
    </div>
  );
}