import { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { fetchUserStats } from '../../api/users'; // создадим этот API позже
import styles from './ProfilePage.module.css';

// Функция для получения первой буквы имени или email
const getInitials = (user) => {
  if (user.first_name && user.last_name) {
    return `${user.first_name[0]}${user.last_name[0]}`;
  }
  if (user.first_name) {
    return user.first_name[0];
  }
  if (user.email) {
    return user.email[0].toUpperCase();
  }
  return '?';
};

// Функция для получения роли на русском
const getRoleDisplay = (role) => {
  switch (role) {
    case 0:
      return { text: 'Администратор', className: styles.badgeAdmin };
    case 1:
      return { text: 'Работник', className: styles.badgeWorker };
    case 2:
      return { text: 'Пользователь', className: styles.badgeUser };
    default:
      return { text: 'Неизвестно', className: '' };
  }
};

export default function ProfilePage() {
  const { user, token } = useAuth();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const loadStats = async () => {
      if (!user) return;
      
      setLoading(true);
      try {
        // Здесь будет API для получения статистики пользователя
        // const data = await fetchUserStats(token);
        // setStats(data);
        
        // Пока используем тестовые данные
        setStats({
          ordersCount: 12,
          carsCount: 3,
          worksCount: 45
        });
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadStats();
  }, [user, token]);

  if (!user) {
    return <div className={styles.error}>Пользователь не найден</div>;
  }

  const role = getRoleDisplay(user.role);
  const initials = getInitials(user);

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Профиль</h1>

      <div className={styles.card}>
        <div className={styles.header}>
          <div className={styles.avatar}>
            {initials}
          </div>
          <div className={styles.name}>
            {user.first_name || user.last_name 
              ? `${user.first_name || ''} ${user.last_name || ''}`.trim()
              : 'Пользователь'}
          </div>
          <div className={`${styles.role} ${role.className}`}>
            {role.text}
          </div>
        </div>

        <div className={styles.content}>
          <div className={styles.section}>
            <h2 className={styles.sectionTitle}>Контактная информация</h2>
            <div className={styles.infoGrid}>
              <div className={styles.infoItem}>
                <span className={styles.infoLabel}>Email</span>
                <span className={styles.infoValue}>{user.email}</span>
              </div>
              <div className={styles.infoItem}>
                <span className={styles.infoLabel}>Телефон</span>
                <span className={styles.infoValue}>{user.phone_number || '—'}</span>
              </div>
              <div className={styles.infoItem}>
                <span className={styles.infoLabel}>Telegram</span>
                <span className={styles.infoValue}>{user.tg_login || '—'}</span>
              </div>
            </div>
          </div>

          <div className={styles.section}>
            <h2 className={styles.sectionTitle}>Статистика</h2>
            {loading ? (
              <div className={styles.loading}>Загрузка статистики...</div>
            ) : error ? (
              <div className={styles.error}>{error}</div>
            ) : stats ? (
              <div className={styles.stats}>
                <div className={styles.statCard}>
                  <div className={styles.statValue}>{stats.ordersCount}</div>
                  <div className={styles.statLabel}>Заказов</div>
                </div>
                <div className={styles.statCard}>
                  <div className={styles.statValue}>{stats.carsCount}</div>
                  <div className={styles.statLabel}>Машин</div>
                </div>
                <div className={styles.statCard}>
                  <div className={styles.statValue}>{stats.worksCount}</div>
                  <div className={styles.statLabel}>Работ</div>
                </div>
              </div>
            ) : (
              <p>Нет данных</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}