import { useEffect, useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { fetchUsers } from '../../api/users';
import { Link } from 'react-router-dom';
import styles from './UsersPage.module.css';

const ROLE_MAP = {
  0: 'Администратор',
  1: 'Работник',
  2: 'Пользователь'
};

export default function UsersPage() {
  const { token, user } = useAuth();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const isAdmin = user?.role === 0;
  const isWorker = user?.role === 1;
  const canView = isAdmin || isWorker;

  useEffect(() => {
    if (!canView) return;
    
    fetchUsers(token)
      .then(data => {
        setUsers(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [token, canView]);

  if (!canView) {
    return <div className={styles.accessDenied}>Доступ запрещён</div>;
  }

  if (loading) return <div className={styles.loading}>Загрузка...</div>;
  if (error) return <div className={styles.error}>Ошибка: {error}</div>;

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Пользователи</h1>
      
      <div className={styles.tableWrapper}>
        <table className={styles.table}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Email</th>
              <th>Имя</th>
              <th>Фамилия</th>
              <th>Телефон</th>
              <th>Telegram</th>
              <th>Роль</th>
              <th>Действия</th>
            </tr>
          </thead>
          <tbody>
            {users.map(u => (
              <tr key={u.id}>
                <td>{u.id}</td>
                <td>{u.email}</td>
                <td>{u.first_name || '—'}</td>
                <td>{u.last_name || '—'}</td>
                <td>{u.phone_number || '—'}</td>
                <td>{u.tg_login || '—'}</td>
                <td>
                  <span className={`${styles.roleBadge} ${styles[`role${u.role}`]}`}>
                    {ROLE_MAP[u.role]}
                  </span>
                </td>
                <td>
                  {isAdmin && (
                    <Link to={`/users/${u.id}/edit`} className={styles.editLink}>
                      Редактировать
                    </Link>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}