export const fetchWorkers = async (token) => {
  const res = await fetch('/api/users/', {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {}
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Ошибка загрузки пользователей');
  
  // Фильтруем только работников (role = 1)
  const workers = (data.results || data).filter(user => user.role === 1);
  return workers;
};