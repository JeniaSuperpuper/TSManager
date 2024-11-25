// import React, { useEffect, useState } from 'react';
// import io from 'socket.io-client';
// import ChatList from './ChatList';


// const socket = io('ws://0.0.0.0:8000/ws/chat/');

// function Chat() {
//   const [messages, setMessages] = useState([]);
//   const [newMessage, setNewMessage] = useState('');

//   useEffect(() => {
//     socket.on('chat_message', (message) => {
//       setMessages((prevMessages) => [...prevMessages, message]);
//     });

//     return () => {
//       socket.disconnect();
//     };
//   }, []);

//   const sendMessage = () => {
//     socket.emit('chat_message', newMessage);
//     setNewMessage('');
//   };

//   return (
//     <div>
//       <h1>Chat</h1>
//       <ChatList messages={messages} />
//       <input
//         type="text"
//         value={newMessage}
//         onChange={(e) => setNewMessage(e.target.value)}
//       />
//       <button onClick={sendMessage}>Send</button>
//     </div>
//   );
// }

// export default Chat;