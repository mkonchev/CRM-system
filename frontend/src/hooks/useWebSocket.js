import { useEffect, useRef, useState, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';

export const useWebSocket = (orderId) => {
  const { token, user } = useAuth();
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState(null);
  const [messages, setMessages] = useState([]);
  const wsRef = useRef(null);

  useEffect(() => {
    if (!token || !orderId) return;

    const wsUrl = `ws://localhost:8000/ws/order/${orderId}/?token=${token}`;
    const ws = new WebSocket(wsUrl);

    wsRef.current = ws;

    ws.onopen = () => {
      console.log('WebSocket connected');
      setIsConnected(true);
      setError(null);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.type === 'chat_message') {
          setMessages(prev => {
            const filtered = prev.filter(msg => 
              !(msg.isTemp && msg.message === data.message)
            );
            return [...filtered, {
              id: data.id || Date.now(),
              message: data.message,
              sender_name: data.sender_name,
              sender_email: data.sender_email,
              timestamp: data.timestamp || new Date().toISOString()
            }];
          });
        }

        if (data.type === 'connection_established') {
          console.log('WS:', data.message);
        }

        if (data.type === 'error') {
          setError(data.message);
        }
      } catch (e) {
        console.error('WS parse error:', e);
      }
    };

    ws.onerror = () => {
      setError('Ошибка WebSocket соединения');
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
      setIsConnected(false);
    };

    return () => {
      if (ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    };
  }, [orderId, token]);

  const sendMessage = useCallback((messageText) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      const tempMessage = {
        id: `temp-${Date.now()}`,
        message: messageText,
        sender_name: user?.username || user?.name || 'Вы',
        sender_email: user?.email,
        timestamp: new Date().toISOString(),
        isTemp: true
      };

      setMessages(prev => [...prev, tempMessage]);

      wsRef.current.send(JSON.stringify({ 
        message: messageText,
        type: 'chat_message'
      }));
      
      return true;
    }
    return false;
  }, [user]);

  return { messages, sendMessage, isConnected, error };
};
