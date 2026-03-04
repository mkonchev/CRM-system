import { useAuth } from '../../context/AuthContext';
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
  const { user } = useAuth();

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
        </div>
      </div>
    </div>
  );
}