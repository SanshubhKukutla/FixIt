import React from 'react';
import { useChat } from '@nlxai/chat-react';
import { chatConfig } from '../../config/chatConfig';
import './styles.modules.css';

const ChatBot = () => {
  const chat = useChat({
    botUrl: chatConfig.botUrl,
    headers: chatConfig.headers,
    languageCode: chatConfig.languageCode,
    userId: `user-${Math.random().toString(36).substr(2, 9)}`, // Generate random user ID
    context: {},
  });

  const handleSendMessage = () => {
    if (chat.inputValue.trim()) {
      chat.conversationHandler.sendText(chat.inputValue);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !chat.waiting) {
      handleSendMessage();
    }
  };

  return (
    <div className="chatContainer">
      <h2>Chatbot</h2>
      <div 
        className="messageList"
        ref={chat.messagesContainerRef}
      >
        {chat.responses.map((message, index) => (
          <div 
            key={index} 
            className={`message ${message.type === 'user' ? 'user-message' : 'bot-message'}`}
          >
            <strong>{message.type === 'user' ? 'You: ' : 'Bot: '}</strong>
            {message.type === 'user' ? message.text : message.payload.text}
          </div>
        ))}
        {chat.waiting && (
          <div className="message bot-message">Bot is typing...</div>
        )}
      </div>
      <div className="inputContainer">
        <input
          className="messageInput"
          type="text"
          value={chat.inputValue}
          onChange={(e) => chat.setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type a message..."
          disabled={chat.waiting}
        />
        <button 
          className="sendButton" 
          onClick={handleSendMessage}
          disabled={chat.waiting || !chat.inputValue.trim()}
        >
          {chat.waiting ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  );
};

export default ChatBot;