// hooks/useWebSocket.js
import { useEffect, useState, useRef } from 'react';

const useWebSocket = (url) => {
    const [messages, setMessages] = useState([]);
    const socket = useRef(null);

    useEffect(() => {
        // Создание WebSocket соединения
        socket.current = new WebSocket(url);

        // Обработка события открытия соединения
        socket.current.onopen = () => {
            console.log('WebSocket connection established.');
        };

        // Обработка полученных сообщений
        socket.current.onmessage = (event) => {
            const message = JSON.parse(event.data);
            setMessages((prevMessages) => [...prevMessages, message]);
        };

        // Обработка события закрытия соединения
        socket.current.onclose = (event) => {
            console.log('WebSocket connection closed:', event);
        };

        // Обработка ошибок
        socket.current.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        // Очистка при размонтировании компонента
        return () => {
            if (socket.current) {
                socket.current.close();
            }
        };
    }, [url]);

    // Функция для отправки сообщения
    const sendMessage = (message) => {
        if (socket.current && socket.current.readyState === WebSocket.OPEN) {
            socket.current.send(JSON.stringify(message));
        }
    };

    return { messages, sendMessage };
};

export default useWebSocket;