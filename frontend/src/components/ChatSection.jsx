import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, X, Brain } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ChatSection = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm psychMASTER, your AI companion for mental health support. How are you feeling today?",
      isBot: true,
      timestamp: new Date()
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [error, setError] = useState(null);
  const [scrollLocked, setScrollLocked] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  };

  useEffect(() => {
    // Only scroll within the chat messages container when not locked
    if (!scrollLocked) {
      const chatContainer = document.getElementById('chat-messages');
      if (chatContainer && messagesEndRef.current) {
        // Smooth scroll to bottom of chat container only, don't affect page scroll
        const scrollTop = chatContainer.scrollHeight - chatContainer.clientHeight;
        chatContainer.scrollTo({
          top: scrollTop,
          behavior: 'smooth'
        });
      }
    }
  }, [messages, scrollLocked]);

  // Handle Enter key press
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      e.stopPropagation();
      
      // Prevent any scroll changes
      const currentScrollY = window.scrollY;
      
      handleSendMessage(e);
      
      // Ensure scroll position stays the same
      setTimeout(() => {
        window.scrollTo(0, currentScrollY);
      }, 0);
    }
  };
  useEffect(() => {
    const initSession = async () => {
      try {
        const response = await axios.post(`${API}/chat/session`, {
          action: "create"
        });
        setSessionId(response.data.session_id);
      } catch (error) {
        console.error('Failed to create session:', error);
        setError('Failed to initialize chat session');
      }
    };
    
    initSession();
  }, []);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (!inputText.trim()) return;

    // Lock scroll position
    const scrollY = window.scrollY;
    setScrollLocked(true);
    
    // Temporarily disable scroll restoration
    if ('scrollRestoration' in history) {
      history.scrollRestoration = 'manual';
    }

    const userMessage = {
      id: Date.now(),
      text: inputText,
      isBot: false,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    const currentMessage = inputText;
    setInputText('');
    setIsTyping(true);
    setError(null);

    try {
      // Send message to AI backend
      const response = await axios.post(`${API}/chat`, {
        message: currentMessage,
        session_id: sessionId
      });

      const botResponse = {
        id: Date.now() + 1,
        text: response.data.response,
        isBot: true,
        timestamp: new Date(),
        isCrisis: response.data.is_crisis || false
      };
      
      setMessages(prev => [...prev, botResponse]);
      
      // Update session ID if returned
      if (response.data.session_id && response.data.session_id !== sessionId) {
        setSessionId(response.data.session_id);
      }
      
    } catch (error) {
      console.error('Chat error:', error);
      
      const errorMessage = {
        id: Date.now() + 1,
        text: "I'm experiencing some technical difficulties right now. Please try again in a moment. If you're in crisis, please call 988 or your local emergency services.",
        isBot: true,
        timestamp: new Date(),
        isError: true
      };
      
      setMessages(prev => [...prev, errorMessage]);
      setError('Connection error - please try again');
    } finally {
      setIsTyping(false);
      
      // Restore original scroll position after a short delay
      setTimeout(() => {
        window.scrollTo(0, scrollY);
        setScrollLocked(false);
        if ('scrollRestoration' in history) {
          history.scrollRestoration = 'auto';
        }
      }, 100);
    }
  };

  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <section id="chat" className="py-20 bg-white">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-4xl lg:text-5xl font-bold text-black mb-6">
            Start Your 
            <span className="bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
              {" "}Conversation
            </span>
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto leading-relaxed">
            Begin your mental health journey with our empathetic AI. Share what's on your mind in a safe, supportive environment.
          </p>
        </div>

        <div className="bg-gray-50 rounded-2xl shadow-2xl overflow-hidden border border-gray-200 relative">
          {/* Chat Header */}
          <div className="bg-black text-white p-6 border-b border-gray-700">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center">
                <Bot className="text-black" size={20} />
              </div>
              <div>
                <h3 className="font-semibold">psychMASTER</h3>
                <p className="text-sm text-gray-300">AI Mental Health Companion</p>
              </div>
              <div className="ml-auto">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  <span className="text-sm text-gray-300">Online</span>
                </div>
              </div>
            </div>
          </div>

          {/* Messages Container */}
          <div className="h-96 overflow-y-auto p-6 space-y-4 bg-white scroll-smooth" id="chat-messages">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.isBot ? 'justify-start' : 'justify-end'} space-x-3`}
              >
                {message.isBot && (
                  <div className="w-8 h-8 bg-black rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                    <Bot className="text-white" size={16} />
                  </div>
                )}
                
                <div className={`max-w-xs lg:max-w-md ${message.isBot ? 'order-2' : 'order-1'}`}>
                  <div
                    className={`rounded-2xl px-4 py-3 ${
                      message.isBot
                        ? message.isCrisis 
                          ? 'bg-red-50 border border-red-200 text-red-900'
                          : message.isError
                          ? 'bg-yellow-50 border border-yellow-200 text-yellow-900'
                          : 'bg-gray-100 text-gray-900'
                        : 'bg-black text-white'
                    }`}
                  >
                    <p className="text-sm leading-relaxed whitespace-pre-line">{message.text}</p>
                    {message.isCrisis && (
                      <div className="mt-2 text-xs text-red-700 font-semibold">
                        🚨 Crisis support information provided above
                      </div>
                    )}
                  </div>
                  <p className={`text-xs text-gray-500 mt-1 ${message.isBot ? 'text-left' : 'text-right'}`}>
                    {formatTime(message.timestamp)}
                  </p>
                </div>

                {!message.isBot && (
                  <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center flex-shrink-0 mt-1 order-2">
                    <User className="text-gray-600" size={16} />
                  </div>
                )}
              </div>
            ))}
            
            {isTyping && (
              <div className="flex justify-start space-x-3">
                <div className="w-8 h-8 bg-black rounded-full flex items-center justify-center flex-shrink-0">
                  <Bot className="text-white" size={16} />
                </div>
                <div className="bg-gray-100 rounded-2xl px-4 py-3">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Form */}
          <form onSubmit={handleSendMessage} className="p-6 border-t border-gray-200 bg-gray-50">
            {error && (
              <div className="mb-3 text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg p-2">
                {error}
              </div>
            )}
            <div className="flex space-x-4">
              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    e.stopPropagation();
                    
                    // Store current scroll position
                    const currentY = window.scrollY;
                    
                    // Handle the message sending
                    handleSendMessage(e);
                    
                    // Immediately restore scroll position
                    requestAnimationFrame(() => {
                      window.scrollTo(0, currentY);
                    });
                  }
                }}
                placeholder="Share what's on your mind..."
                className="flex-1 px-4 py-3 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent"
                disabled={isTyping || !sessionId}
              />
              <button
                type="submit"
                disabled={!inputText.trim() || isTyping || !sessionId}
                className="bg-black text-white px-6 py-3 rounded-xl hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-black focus:ring-offset-2 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Send size={20} />
              </button>
            </div>
            {!sessionId && (
              <p className="text-xs text-gray-500 mt-2">Connecting to AI companion...</p>
            )}
          </form>
        </div>

        <div className="mt-8 text-center">
          <p className="text-sm text-gray-500 max-w-2xl mx-auto">
            <strong>Disclaimer:</strong> This AI tool is for awareness and support purposes only. 
            It is not a substitute for professional medical advice, diagnosis, or treatment. 
            If you're experiencing a mental health crisis, please contact a healthcare professional or emergency services.
          </p>
        </div>
      </div>
    </section>
  );
};

export default ChatSection;