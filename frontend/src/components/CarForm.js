import { useState } from 'react';

export default function CarForm({ onCarCreated }) {
  const [mark, setMark] = useState('');
  const [model, setModel] = useState('');
  const [year, setYear] = useState('');
  const [number, setNumber] = useState('');
  const [vin, setVin] = useState('');          // ✅ новое поле
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await onCarCreated({
        mark,
        model,
        year: year ? Number(year) : null,
        number,
        vin: vin || null                         // ✅ передаём VIN
      });
      setMark('');
      setModel('');
      setYear('');
      setNumber('');
      setVin('');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
      <h3>Добавить машину</h3>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxWidth: '400px' }}>
        <input
          placeholder="Марка (можно не заполнять, если есть VIN)"
          value={mark}
          onChange={(e) => setMark(e.target.value)}
        />
        <input
          placeholder="Модель (можно не заполнять, если есть VIN)"
          value={model}
          onChange={(e) => setModel(e.target.value)}
        />
        <input
          placeholder="Год (можно не заполнять, если есть VIN)"
          type="number"
          value={year}
          onChange={(e) => setYear(e.target.value)}
        />
        <input
          placeholder="Госномер"
          value={number}
          onChange={(e) => setNumber(e.target.value)}
        />
        <input
          placeholder="VIN (если ввести, марка/модель/год заполнятся автоматически)"
          value={vin}
          onChange={(e) => setVin(e.target.value)}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Сохранение...' : 'Добавить'}
        </button>
      </div>
    </form>
  );
}