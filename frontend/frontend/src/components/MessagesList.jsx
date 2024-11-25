import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

const MessagesComponent = ({ setMessageCount }) => {
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [userId, setUserId] = useState(null);

    useEffect(() => {
        const checkLoggedIn = () => {
            const accessToken = localStorage.getItem('access_token');
            if (accessToken) {
                setIsLoggedIn(true);
                try {
                    const decodedToken = jwtDecode(accessToken);
                    setUserId(decodedToken.user_id);
                } catch (error) {
                    console.error('Error decoding JWT token:', error);
                }
            }
        };

        checkLoggedIn();
    }, []);

    useEffect(() => {
        const fetchMessages = async () => {
            if (!isLoggedIn || !userId) {
                setLoading(false);
                return;
            }

            try {
                const response = await axios.get('http://127.0.0.1:8000/api/v1/messages/', {
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                    }
                });

                const filteredMessages = response.data.filter(message => message.owner === userId);

                const sortedMessages = filteredMessages.sort((a, b) => new Date(b.created) - new Date(a.created));

                setMessages(sortedMessages);
                setMessageCount(sortedMessages.length);
            } catch (error) {
                setError(error.message);
            } finally {
                setLoading(false);
            }
        };

        fetchMessages();

        // Устанавливаем интервал для проверки новых сообщений каждые 2 секунды
        const intervalId = setInterval(fetchMessages, 2000);

        return () => clearInterval(intervalId);
    }, [isLoggedIn, userId, setMessageCount]);

    const handleDeleteMessage = async (messageId) => {
        try {
            await axios.delete(`http://127.0.0.1:8000/api/v1/messages/delete/${messageId}`, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                }
            });

            const updatedMessages = messages.filter(message => message.id !== messageId);
            setMessages(updatedMessages);
            setMessageCount(updatedMessages.length);
        } catch (error) {
            setError('Ошибка при удалении сообщения');
        }
    };

    if (!isLoggedIn) {
        return <div>Please log in to view your messages.</div>;
    }

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div className='mesage__block'>
            <h1 className='message_text'>Your Messages</h1>
            {messages.length === 0 ? (
                <div className='message_text'>У Вас пока нет сообщений</div>
            ) : (
                <ul>
                    {messages.map(message => (
                        <li key={message.id}>
                            <h2 className='message_text'>{message.title}</h2>
                            <p className='message_text'>{message.text}</p>
                            <button className='delete-button button message_button' onClick={() => handleDeleteMessage(message.id)}>Удалить</button>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default MessagesComponent;