export const fetchOrders = async (token) => {
  const res = await fetch('/api/orders/', {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {}
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Ошибка загрузки заказов');
  return data.results || data;
};

export const fetchOrderById = async (token, id) => {
  const res = await fetch(`/api/orders/${id}/`, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {}
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Ошибка загрузки заказа');
  return data;
};

export const updateWorkStatus = async (token, workstatusId, status) => {
  const res = await fetch(`/api/workstatus/${workstatusId}/`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ status })
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Ошибка обновления статуса');
  return data;
};

export const createOrder = async (token, orderData) => {
  const res = await fetch('/api/orders/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(orderData)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Ошибка создания заказа');
  return data;
};