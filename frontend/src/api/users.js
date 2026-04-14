export const fetchUsers = async (token) => {
  const res = await fetch('/api/users/', {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {}
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Ошибка загрузки пользователей');
  return data.results || data;
};

export const fetchWorkers = async (token) => {
  const users = await fetchUsers(token);
  return users.filter(user => user.role === 1);
};

export const fetchUserById = async (token, id) => {
  const res = await fetch(`/api/users/${id}/`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {}
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Ошибка загрузки пользователя');
  return data;
};

export const updateUserProfile = async (token, userId, userData) => {
  const res = await fetch(`/api/users/${userId}/`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {})
    },
    body: JSON.stringify(userData)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Ошибка обновления профиля');
  return data;
};