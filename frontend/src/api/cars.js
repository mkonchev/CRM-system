export const fetchCars = async (token) => {
  const res = await fetch('/api/cars/', {
    headers: { 'Authorization': `Bearer ${token}` }
  });
  const data = await res.json();
  
  if (!res.ok) {
    throw new Error(data.detail || 'Ошибка загрузки');
  }
  
  return data.results || data; // ← возвращаем массив
};
export const createCar = async (token, carData) => {
  const res = await fetch('/api/cars/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(carData)
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.detail || 'Ошибка создания');
  return data;
};
export const deleteCar = async (token, carId) => {
  const res = await fetch(`/api/cars/${carId}/`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.detail || 'Ошибка удаления');
  }
  return true;
};