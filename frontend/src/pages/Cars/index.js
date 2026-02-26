import { useEffect, useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { fetchCars, createCar, deleteCar } from '../../api/cars';  // ✅ импорт deleteCar
import CarForm from '../../components/CarForm';

export default function CarsPage() {
  const { token } = useAuth();
  const [cars, setCars] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const loadCars = () => {
    fetchCars(token)
      .then(data => {
        setCars(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  };

  const handleCarCreated = async (carData) => {
    await createCar(token, carData);
    loadCars();
  };

  const handleDelete = async (carId) => {
    if (!window.confirm('Удалить машину?')) return;
    try {
      await deleteCar(token, carId);
      loadCars();  // перезагружаем список после удаления
    } catch (err) {
      alert(err.message);
    }
  };

  useEffect(() => {
    loadCars();
  }, []);

  if (loading) return <div>Загрузка...</div>;
  if (error) return <div style={{ color: 'red' }}>Ошибка: {error}</div>;

  return (
    <div>
      <h1>Мои машины</h1>
      <CarForm onCarCreated={handleCarCreated} />
      {cars.length === 0 ? (
        <p>Нет машин</p>
      ) : (
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {cars.map(car => (
            <li key={car.id} style={{
              border: '1px solid #ccc',
              margin: '10px 0',
              padding: '10px',
              borderRadius: '5px'
            }}>
              <div>
                <strong>{car.mark} {car.model}</strong> ({car.year})
              </div>
              <div>Номер: {car.number || '—'}</div>
              <div>VIN: {car.vin || '—'}</div>
              <button
                onClick={() => handleDelete(car.id)}
                style={{
                  marginTop: '10px',
                  backgroundColor: '#dc3545',
                  color: 'white',
                  border: 'none',
                  padding: '5px 10px',
                  borderRadius: '3px',
                  cursor: 'pointer'
                }}
              >
                Удалить
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}