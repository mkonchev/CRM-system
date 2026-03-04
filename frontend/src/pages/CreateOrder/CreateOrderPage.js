import { useEffect, useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { fetchCars } from '../../api/cars';
import { fetchWorks, createWork } from '../../api/works';
import { createOrder } from '../../api/orders';
import { fetchUsers } from '../../api/users';
import NewWorkForm from '../../components/NewWorkForm/NewWorkForm';
import WorkItem from '../../components/WorkItem/WorkItem';
import styles from './CreateOrderPage.module.css';

export default function CreateOrderPage() {
  const { token } = useAuth();
  const [cars, setCars] = useState([]);
  const [works, setWorks] = useState([]);
  const [workers, setWorkers] = useState([]);
  const [selectedCar, setSelectedCar] = useState('');
  const [selectedWorker, setSelectedWorker] = useState('');
  const [selectedWorks, setSelectedWorks] = useState({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [showNewWorkForm, setShowNewWorkForm] = useState(false);

  useEffect(() => {
    Promise.all([
      fetchCars(token),
      fetchWorks(token),
      fetchUsers(token)
    ])
      .then(([carsData, worksData, usersData]) => {
        setCars(carsData);
        setWorks(worksData);
        setWorkers(usersData.filter(u => u.role === 1));
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [token]);

  const handleWorkToggle = (workId) => {
    setSelectedWorks(prev => {
      const newSelected = { ...prev };
      if (newSelected[workId]) {
        delete newSelected[workId];
      } else {
        newSelected[workId] = 1;
      }
      return newSelected;
    });
  };

  const handleQuantityChange = (workId, newQuantity) => {
    if (newQuantity < 1) {
      setSelectedWorks(prev => {
        const newSelected = { ...prev };
        delete newSelected[workId];
        return newSelected;
      });
    } else {
      setSelectedWorks(prev => ({
        ...prev,
        [workId]: newQuantity
      }));
    }
  };

  const handleCreateWork = async (workData) => {
    try {
      const newWork = await createWork(token, workData);
      setWorks(prev => [...prev, newWork]);
      setSelectedWorks(prev => ({
        ...prev,
        [newWork.id]: 1
      }));
      setShowNewWorkForm(false);
    } catch (err) {
      alert('Ошибка при создании работы: ' + err.message);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedCar || !selectedWorker || Object.keys(selectedWorks).length === 0) {
      alert('Заполните все поля');
      return;
    }

    setSubmitting(true);
    try {
      const order = await createOrder(token, {
        car: parseInt(selectedCar),
        worker: parseInt(selectedWorker)
      });

      await Promise.all(Object.entries(selectedWorks).map(async ([workId, quantity]) => {
        const response = await fetch('/api/workstatus/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            order: order.id,
            work: parseInt(workId),
            amount: quantity,
            status: 0
          })
        });

        if (!response.ok) {
          const data = await response.json();
          throw new Error(JSON.stringify(data));
        }
      }));

      alert('Заказ создан!');
      setSelectedCar('');
      setSelectedWorker('');
      setSelectedWorks({});
    } catch (err) {
      alert(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  const totalPrice = Object.entries(selectedWorks).reduce((sum, [workId, quantity]) => {
    const work = works.find(w => w.id === parseInt(workId));
    return sum + (work?.price || 0) * quantity;
  }, 0);

  const getWorkDisplayName = (work) => {
    if (!work.car) return work.name;
    const car = cars.find(c => c.id === work.car);
    return car ? `${work.name} (${car.mark} ${car.model} ${car.year})` : work.name;
  };

  if (loading) return <div className={styles.loading}>Загрузка...</div>;
  if (error) return <div className={styles.error}>Ошибка: {error}</div>;

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Создание заказа</h1>
      
      <form onSubmit={handleSubmit}>
        <div className={styles.section}>
          <h3 className={styles.sectionTitle}>Выберите машину</h3>
          <select
            value={selectedCar}
            onChange={(e) => setSelectedCar(e.target.value)}
            className={styles.select}
          >
            <option value="">-- Выберите машину --</option>
            {cars.map(car => (
              <option key={car.id} value={car.id}>
                {car.mark} {car.model} ({car.year}) - {car.number || 'без номера'}
              </option>
            ))}
          </select>
        </div>

        <div className={styles.section}>
          <h3 className={styles.sectionTitle}>Выберите работника</h3>
          <select
            value={selectedWorker}
            onChange={(e) => setSelectedWorker(e.target.value)}
            className={styles.select}
          >
            <option value="">-- Выберите работника --</option>
            {workers.map(worker => (
              <option key={worker.id} value={worker.id}>
                {worker.first_name} {worker.last_name} ({worker.email})
              </option>
            ))}
          </select>
        </div>

        <div className={styles.section}>
          <div className={styles.worksHeader}>
            <h3 className={styles.sectionTitle}>Выберите работы</h3>
            <button
              type="button"
              onClick={() => setShowNewWorkForm(true)}
              className={styles.addWorkButton}
            >
              ➕ Новая работа
            </button>
          </div>

          {showNewWorkForm && (
            <NewWorkForm
              cars={cars}
              onSubmit={handleCreateWork}
              onCancel={() => setShowNewWorkForm(false)}
            />
          )}

          <div className={styles.worksList}>
            {works.map(work => (
              <WorkItem
                key={work.id}
                work={work}
                isSelected={!!selectedWorks[work.id]}
                quantity={selectedWorks[work.id]}
                displayName={getWorkDisplayName(work)}
                onToggle={handleWorkToggle}
                onQuantityChange={handleQuantityChange}
              />
            ))}
          </div>
        </div>

        {Object.keys(selectedWorks).length > 0 && (
          <div className={styles.totalSection}>
            <h3 className={styles.totalPrice}>Итого: {totalPrice} ₽</h3>
          </div>
        )}

        <button
          type="submit"
          disabled={submitting || !selectedCar || !selectedWorker || Object.keys(selectedWorks).length === 0}
          className={styles.submitButton}
        >
          {submitting ? 'Создание...' : 'Создать заказ'}
        </button>
      </form>
    </div>
  );
}