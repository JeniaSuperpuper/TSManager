import React from 'react';

function ChatList({ messages }) {
  return (
    <div>
      {messages.map((message, index) => (
        <div key={index}>
          <p>{message}</p>
        </div>
      ))}
    </div>
  );
}

export default ChatList;