import { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { login } from '../../api/auth';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login: authLogin } = useAuth();

    const handleSubmit = async (e) => {
    e.preventDefault();
    const data = await login(email, password);
    if (data.access) {
        authLogin(data.access, data.user); // ← сохраняем пользователя
    } else {
        setError('Неверный email или пароль');
    }
    };

  return (
    <div>
      <h2>Вход</h2>
      <form onSubmit={handleSubmit}>
        <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <input type="password" placeholder="Пароль" value={password} onChange={(e) => setPassword(e.target.value)} required />
        {error && <p>{error}</p>}
        <button type="submit">Войти</button>
      </form>
    </div>
  );
}