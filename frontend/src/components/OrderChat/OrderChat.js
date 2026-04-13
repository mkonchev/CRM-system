import { useState, useEffect, useRef } from 'react';
import { useWebSocket } from '../../hooks/useWebSocket';
import { fetchChatHistory } from '../../api/chat';
import { useAuth } from '../../context/AuthContext';
import styles from './OrderChat.module.css';

export default function OrderChat({ orderId }) {
  const { token } = useAuth();
  const [inputMessage, setInputMessage] = useState('');
  const [history, setHistory] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(true);
  const messagesEndRef = useRef(null);
  
  const { messages, sendMessage, isConnected, error } = useWebSocket(orderId);

  useEffect(() => {
    const loadHistory = async () => {
      try {
        const data = await fetchChatHistory(token, orderId);
        setHistory(data);
      } catch (err) {
        console.error('Failed to load chat history:', err);
      } finally {
        setLoadingHistory(false);
      }
    };
    loadHistory();
  }, [orderId, token]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, history]);

  const handleSend = (e) => {
    e.preventDefault();
    if (inputMessage.trim() && sendMessage(inputMessage.trim())) {
      setInputMessage('');
    }
  };

  const allMessages = [...history, ...messages];

  return (
    <div className={styles.chatContainer}>
      <div className={styles.header}>
        <h3>Чат по заказу #{orderId}</h3>
        <div className={`${styles.status} ${isConnected ? styles.online : styles.offline}`}>
          {isConnected ? '🟢 В сети' : '🔴 Не в сети'}
        </div>
      </div>

      <div className={styles.messagesList}>
        {loadingHistory && <div className={styles.loading}>Загрузка истории...</div>}
        {allMessages.length === 0 && !loadingHistory && (
          <div className={styles.empty}>Нет сообщений</div>
        )}
        {allMessages.map((msg, idx) => (
          <div key={msg.id || idx} className={styles.message}>
            <div className={styles.messageHeader}>
              <span className={styles.sender}>{msg.sender_name || msg.sender_email}</span>
              <span className={styles.time}>
                {new Date(msg.timestamp).toLocaleTimeString()}
              </span>
            </div>
            <div className={styles.messageBody}>{msg.message}</div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSend} className={styles.inputForm}>
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder={isConnected ? "Введите сообщение..." : "Нет подключения"}
          disabled={!isConnected}
          className={styles.input}
        />
        <button type="submit" disabled={!isConnected} className={styles.button}>
          Отправить
        </button>
      </form>
      {error && <div className={styles.error}>{error}</div>}
    </div>
  );
}