import { useEffect, useState } from 'react';

function App() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetch('/api/')
      .then(res => res.json())
      .then(data => setMessage(JSON.stringify(data)))
      .catch(err => setMessage('Ошибка: ' + err.message));
  }, []);

  return (
    <div>
      <h1>CRM Frontend</h1>
      <p>Ответ от бэкенда: {message}</p>
    </div>
  );
}

export default App;