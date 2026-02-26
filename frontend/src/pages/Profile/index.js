import { useAuth } from '../../context/AuthContext';

export default function ProfilePage() {
  const { user } = useAuth();

  return (
    <div>
      <h1>Профиль</h1>
      <p>Email: {user?.email || 'Неизвестно'}</p>
    </div>
  );
}