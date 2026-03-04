import { useState } from 'react';
import styles from './NewWorkForm.module.css';

export default function NewWorkForm({ cars, onSubmit, onCancel }) {
  const [name, setName] = useState('');
  const [price, setPrice] = useState('');
  const [description, setDescription] = useState('');
  const [carId, setCarId] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      name,
      price: parseInt(price),
      description: description || undefined,
      car: carId ? parseInt(carId) : null
    });
  };

  return (
    <form onSubmit={handleSubmit} className={styles.form}>
      <h4>Создание новой работы</h4>
      
      <div className={styles.formGroup}>
        <input
          type="text"
          placeholder="Название работы *"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className={styles.input}
          required
        />
      </div>

      <div className={styles.formGroup}>
        <input
          type="number"
          placeholder="Цена *"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
          className={styles.input}
          required
        />
      </div>

      <div className={styles.formGroup}>
        <textarea
          placeholder="Описание (необязательно)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className={styles.textarea}
        />
      </div>

      <div className={styles.formGroup}>
        <label className={styles.label}>
          Привязать к машине (необязательно):
        </label>
        <select
          value={carId}
          onChange={(e) => setCarId(e.target.value)}
          className={styles.select}
        >
          <option value="">-- Нет привязки (общая работа) --</option>
          {cars.map(car => (
            <option key={car.id} value={car.id}>
              {car.mark} {car.model} ({car.year}) - {car.number || 'без номера'}
            </option>
          ))}
        </select>
      </div>

      <div className={styles.actions}>
        <button type="submit" className={styles.createButton}>
          Создать
        </button>
        <button type="button" onClick={onCancel} className={styles.cancelButton}>
          Отмена
        </button>
      </div>
    </form>
  );
}