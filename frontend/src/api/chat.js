export const fetchChatHistory = async (token, orderId) => {
  const res = await fetch(`/api/history/${orderId}/`, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });
  if (!res.ok) throw new Error('Ошибка загрузки истории');
  const data = await res.json();
  return data.results || data || [];
};