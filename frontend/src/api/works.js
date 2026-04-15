export const fetchWorks = async (token, filters = {}) => {
  const params = new URLSearchParams();
  if (filters.mark) params.append('mark', filters.mark);
  
  const url = `/api/works/${params.toString() ? '?' + params.toString() : ''}`;
  
  const res = await fetch(url, {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {}
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Ошибка загрузки работ');
  return data.results || data;
};

export const createWork = async (token, workData) => {
  const res = await fetch('/api/works/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(workData)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Ошибка создания работы');
  return data;
};

export const fetchGroupedWorks = async (token) => {
  const res = await fetch('/api/works/grouped/', {
    headers: token ? { 'Authorization': `Bearer ${token}` } : {}
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Ошибка загрузки работ');
  return data;
};