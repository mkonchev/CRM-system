import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { fetchUserById, updateUserProfile } from '../../api/users';
import Input from '../../components/Input/Input';
import Button from '../../components/Button/Button';
import styles from './UserEdit.module.css';

const ROLE_OPTIONS = [
  { value: 0, label: 'Администратор' },
  { value: 1, label: 'Работник' },
  { value: 2, label: 'Пользователь' }
];

export default function UserEdit() {
  const { id } = useParams();
  const { token, user: currentUser } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [formData, setFormData] = useState({
    email: '',
    first_name: '',
    last_name: '',
    phone_number: '',
    tg_login: '',
    role: 2
  });

  useEffect(() => {
    if (currentUser?.role !== 0) {
      setLoading(false);
      return;
    }
    
    fetchUserById(token, id)
      .then(data => {
        setFormData({
          email: data.email || '',
          first_name: data.first_name || '',
          last_name: data.last_name || '',
          phone_number: data.phone_number || '',
          tg_login: data.tg_login || '',
          role: data.role ?? 2
        });
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [token, id, currentUser?.role]);

  if (currentUser?.role !== 0) {
    return <div className={styles.accessDenied}>Доступ запрещён</div>;
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError('');
    setSuccess('');

    try {
      await updateUserProfile(token, id, formData);
      setSuccess('Пользователь обновлён!');
      setTimeout(() => navigate('/users'), 1500);
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className={styles.loading}>Загрузка...</div>;

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Редактирование пользователя</h1>
      
      <form onSubmit={handleSubmit} className={styles.form}>
        <Input
          name="email"
          label="Email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        
        <Input
          name="first_name"
          label="Имя"
          value={formData.first_name}
          onChange={handleChange}
        />
        
        <Input
          name="last_name"
          label="Фамилия"
          value={formData.last_name}
          onChange={handleChange}
        />
        
        <Input
          name="phone_number"
          label="Телефон"
          value={formData.phone_number}
          onChange={handleChange}
        />
        
        <Input
          name="tg_login"
          label="Telegram"
          value={formData.tg_login}
          onChange={handleChange}
        />
        
        <div className={styles.formGroup}>
          <label className={styles.label}>Роль</label>
          <select
            name="role"
            value={formData.role}
            onChange={handleChange}
            className={styles.select}
          >
            {ROLE_OPTIONS.map(opt => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>
        
        {error && <div className={styles.error}>{error}</div>}
        {success && <div className={styles.success}>{success}</div>}
        
        <div className={styles.actions}>
          <Button type="submit" disabled={saving}>
            {saving ? 'Сохранение...' : 'Сохранить'}
          </Button>
          <button
            type="button"
            onClick={() => navigate('/users')}
            className={styles.cancelButton}
          >
            Отмена
          </button>
        </div>
      </form>
    </div>
  );
}