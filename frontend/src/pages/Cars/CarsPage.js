import { useEffect, useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { fetchCars, createCar, deleteCar } from '../../api/cars';
import CarForm from '../../components/CarForm';
import CarCard from '../../components/CarCard/CarCard';
import styles from './CarsPage.module.css';

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
      loadCars();
    } catch (err) {
      alert(err.message);
    }
  };

  useEffect(() => {
    loadCars();
  }, []);

  if (loading) return <div className={styles.loading}>Загрузка...</div>;
  if (error) return <div className={styles.error}>Ошибка: {error}</div>;

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Мои машины</h1>
      <CarForm onCarCreated={handleCarCreated} />
      {cars.length === 0 ? (
        <p className={styles.empty}>Нет машин</p>
      ) : (
        <ul className={styles.list}>
          {cars.map(car => (
            <CarCard key={car.id} car={car} onDelete={handleDelete} />
          ))}
        </ul>
      )}
    </div>
  );
}