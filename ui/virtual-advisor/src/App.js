import React, { useState, useRef, useEffect } from 'react';
import { Send, MessageCircle, BookOpen, User, Settings, Menu, X, Loader2 } from 'lucide-react';

// Configuration - easily extensible for future features
const CONFIG = {
  API_ENDPOINT: '/api/chat', // Replace with your actual endpoint
  MAX_MESSAGES: 100,
  TYPING_DELAY: 50,
  THEMES: {
    primary: 'from-blue-600 to-purple-600',
    secondary: 'from-purple-500 to-pink-500',
    accent: 'from-emerald-500 to-teal-500'
  }
};

// Mock API function - replace with your actual API call
const callLLMAPI = async (message, conversationHistory) => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 1000));
  
  // Mock response based on academic context
  const responses = [
    "Based on your current course load, I'd recommend focusing on your core requirements first. What specific area would you like guidance on?",
    "That's a great question about course planning! Let me help you think through the prerequisites and scheduling considerations.",
    "For your major requirements, you have several interesting options. Here's what I'd suggest based on your academic goals...",
    "I can see you're working on your degree plan. Let's break this down step by step to make sure you're on the right track.",
    "Academic success often comes down to good planning and time management. What specific challenges are you facing?"
  ];
  
  return responses[Math.floor(Math.random() * responses.length)];
};

// Reusable components for extensibility
const Avatar = ({ type, className = "" }) => (
  <div className={`w-8 h-8 rounded-full flex items-center justify-center ${className}`}>
    {type === 'user' ? (
      <User className="w-5 h-5 text-white" />
    ) : (
      <BookOpen className="w-5 h-5 text-white" />
    )}
  </div>
);

const TypingIndicator = () => (
  <div className="flex items-center space-x-1 text-gray-500">
    <div className="flex space-x-1">
      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
    </div>
    <span className="text-sm ml-2">Academic Advisor is typing...</span>
  </div>
);

const Message = ({ message, isUser, timestamp }) => (
  <div className={`flex items-start space-x-3 ${isUser ? 'flex-row-reverse space-x-reverse' : ''} mb-6`}>
    <Avatar 
      type={isUser ? 'user' : 'advisor'} 
      className={isUser ? 'bg-gradient-to-r from-blue-500 to-purple-500' : 'bg-gradient-to-r from-emerald-500 to-teal-500'}
    />
    <div className={`flex-1 ${isUser ? 'text-right' : ''}`}>
      <div className={`inline-block max-w-[85%] px-4 py-3 rounded-2xl shadow-sm ${
        isUser 
          ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white' 
          : 'bg-white border border-gray-100 text-gray-800'
      }`}>
        <p className="text-sm leading-relaxed">{message}</p>
      </div>
      <p className="text-xs text-gray-500 mt-1 px-2">
        {timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
      </p>
    </div>
  </div>
);

const Header = ({ onMenuToggle, isMobileMenuOpen }) => (
  <header className="bg-white shadow-sm border-b border-gray-100 px-4 py-3 flex items-center justify-between">
    <div className="flex items-center space-x-3">
      <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl flex items-center justify-center">
        <BookOpen className="w-6 h-6 text-white" />
      </div>
      <div>
        <h1 className="text-lg font-semibold text-gray-900">Academic Advisor</h1>
        <p className="text-sm text-gray-500">Your AI-powered guidance counselor</p>
      </div>
    </div>
    <button
      onClick={onMenuToggle}
      className="md:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors"
    >
      {isMobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
    </button>
  </header>
);

const Sidebar = ({ isOpen, onClose }) => (
  <>
    {/* Mobile overlay */}
    {isOpen && (
      <div 
        className="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden" 
        onClick={onClose}
      />
    )}
    
    {/* Sidebar */}
    <aside className={`
      fixed left-0 top-0 h-full w-64 bg-white shadow-xl z-50 transform transition-transform duration-300 ease-in-out
      md:relative md:translate-x-0 md:shadow-none md:border-r md:border-gray-200
      ${isOpen ? 'translate-x-0' : '-translate-x-full'}
    `}>
      <div className="p-6">
        <div className="flex items-center space-x-3 mb-8">
          <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
            <BookOpen className="w-5 h-5 text-white" />
          </div>
          <span className="font-semibold text-gray-900">Advisor</span>
        </div>
        
        <nav className="space-y-2">
          <a href="#" className="flex items-center space-x-3 px-3 py-2 rounded-lg bg-blue-50 text-blue-700">
            <MessageCircle className="w-4 h-4" />
            <span className="text-sm font-medium">Chat</span>
          </a>
          <a href="#" className="flex items-center space-x-3 px-3 py-2 rounded-lg text-gray-600 hover:bg-gray-50 transition-colors">
            <User className="w-4 h-4" />
            <span className="text-sm font-medium">Profile</span>
          </a>
          <a href="#" className="flex items-center space-x-3 px-3 py-2 rounded-lg text-gray-600 hover:bg-gray-50 transition-colors">
            <Settings className="w-4 h-4" />
            <span className="text-sm font-medium">Settings</span>
          </a>
        </nav>
      </div>
    </aside>
  </>
);

const ChatInput = ({ message, setMessage, onSend, isLoading }) => (
  <div className="bg-white border-t border-gray-200 p-4">
    <div className="flex items-end space-x-3 max-w-4xl mx-auto">
      <div className="flex-1 relative">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              onSend();
            }
          }}
          placeholder="Ask your academic advisor anything..."
          className="w-full px-4 py-3 border border-gray-300 rounded-2xl resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
          rows="1"
          style={{ minHeight: '44px', maxHeight: '120px' }}
          disabled={isLoading}
        />
      </div>
      <button
        onClick={onSend}
        disabled={!message.trim() || isLoading}
        className={`p-3 rounded-2xl transition-all transform ${
          message.trim() && !isLoading
            ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white hover:scale-105 shadow-lg'
            : 'bg-gray-100 text-gray-400 cursor-not-allowed'
        }`}
      >
        {isLoading ? (
          <Loader2 className="w-5 h-5 animate-spin" />
        ) : (
          <Send className="w-5 h-5" />
        )}
      </button>
    </div>
  </div>
);

const EmptyState = () => (
  <div className="flex-1 flex items-center justify-center p-8">
    <div className="text-center max-w-md">
      <div className="w-16 h-16 bg-gradient-to-r from-blue-100 to-purple-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
        <BookOpen className="w-8 h-8 text-blue-600" />
      </div>
      <h2 className="text-xl font-semibold text-gray-900 mb-2">Welcome to Academic Advisor</h2>
      <p className="text-gray-600 mb-6">
        I'm here to help you with course planning, degree requirements, academic goals, and more. 
        What would you like to discuss today?
      </p>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm">
        <div className="p-3 bg-blue-50 rounded-lg text-blue-700">
          <span className="font-medium">Course Planning</span>
        </div>
        <div className="p-3 bg-purple-50 rounded-lg text-purple-700">
          <span className="font-medium">Degree Requirements</span>
        </div>
        <div className="p-3 bg-emerald-50 rounded-lg text-emerald-700">
          <span className="font-medium">Academic Goals</span>
        </div>
        <div className="p-3 bg-pink-50 rounded-lg text-pink-700">
          <span className="font-medium">Career Guidance</span>
        </div>
      </div>
    </div>
  </div>
);

export default function AcademicAdvisorApp() {
  const [messages, setMessages] = useState([]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSendMessage = async () => {
    if (!currentMessage.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: currentMessage.trim(),
      isUser: true,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setCurrentMessage('');
    setIsLoading(true);
    setIsTyping(true);

    try {
      // Call your LLM API here
      const response = await callLLMAPI(userMessage.text, messages);
      
      setIsTyping(false);
      
      const advisorMessage = {
        id: Date.now() + 1,
        text: response,
        isUser: false,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, advisorMessage]);
    } catch (error) {
      setIsTyping(false);
      const errorMessage = {
        id: Date.now() + 1,
        text: "I apologize, but I'm having trouble connecting right now. Please try again in a moment.",
        isUser: false,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar 
        isOpen={isMobileMenuOpen} 
        onClose={() => setIsMobileMenuOpen(false)} 
      />
      
      <div className="flex-1 flex flex-col min-w-0">
        <Header 
          onMenuToggle={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          isMobileMenuOpen={isMobileMenuOpen}
        />
        
        <main className="flex-1 flex flex-col min-h-0">
          <div className="flex-1 overflow-y-auto">
            {messages.length === 0 ? (
              <EmptyState />
            ) : (
              <div className="max-w-4xl mx-auto p-4 space-y-4">
                {messages.map((msg) => (
                  <Message
                    key={msg.id}
                    message={msg.text}
                    isUser={msg.isUser}
                    timestamp={msg.timestamp}
                  />
                ))}
                {isTyping && (
                  <div className="flex items-start space-x-3 mb-6">
                    <Avatar type="advisor" className="bg-gradient-to-r from-emerald-500 to-teal-500" />
                    <div className="flex-1">
                      <TypingIndicator />
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            )}
          </div>
          
          <ChatInput
            message={currentMessage}
            setMessage={setCurrentMessage}
            onSend={handleSendMessage}
            isLoading={isLoading}
          />
        </main>
      </div>
    </div>
  );
}