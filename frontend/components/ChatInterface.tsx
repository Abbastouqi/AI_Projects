'use client'

import { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import MessageBubble from './MessageBubble'
import LaptopCard from './LaptopCard'
import QuickReplies from './QuickReplies'
import ComparisonView from './ComparisonView'
import { Message, Laptop } from '@/types/chat'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [sessionId, setSessionId] = useState<string>('')
  const [selectedLaptops, setSelectedLaptops] = useState<Laptop[]>([])
  const [showComparison, setShowComparison] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Load session from localStorage
  useEffect(() => {
    const savedSessionId = localStorage.getItem('laptop_chat_session')
    if (savedSessionId) {
      setSessionId(savedSessionId)
      loadSession(savedSessionId)
    } else {
      // Show initial greeting
      setMessages([{
        role: 'assistant',
        content: 'السلام علیکم! Welcome to Pakistan\'s smartest laptop recommendation assistant! 🎓💻\n\nI\'m here to help Pakistani students find the perfect laptop within their budget.\n\nTo get started, tell me:\n1. What will you use the laptop for?\n2. What\'s your budget in PKR?',
        timestamp: new Date().toISOString()
      }])
    }
  }, [])

  const loadSession = async (sid: string) => {
    try {
      const response = await axios.get(`${API_URL}/api/session/${sid}`)
      const history = response.data.conversation_history || []
      setMessages(history.map((msg: any) => ({
        role: msg.role,
        content: msg.content,
        recommendations: msg.recommendations,
        timestamp: msg.timestamp
      })))
    } catch (error) {
      console.error('Error loading session:', error)
    }
  }

  const sendMessage = async (messageText?: string) => {
    const textToSend = messageText || input
    if (!textToSend.trim()) return

    const userMessage: Message = {
      role: 'user',
      content: textToSend,
      timestamp: new Date().toISOString()
    }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await axios.post(`${API_URL}/api/chat`, {
        message: textToSend,
        session_id: sessionId
      })

      const newSessionId = response.data.session_id
      if (!sessionId) {
        setSessionId(newSessionId)
        localStorage.setItem('laptop_chat_session', newSessionId)
      }

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.data.response,
        recommendations: response.data.recommendations,
        timestamp: new Date().toISOString()
      }
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error('Error:', error)
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString()
      }])
    } finally {
      setLoading(false)
    }
  }

  const handleQuickReply = (text: string) => {
    sendMessage(text)
  }

  const handleLaptopSelect = (laptop: Laptop) => {
    if (selectedLaptops.find(l => l.id === laptop.id)) {
      setSelectedLaptops(selectedLaptops.filter(l => l.id !== laptop.id))
    } else if (selectedLaptops.length < 3) {
      setSelectedLaptops([...selectedLaptops, laptop])
    }
  }

  const handleCompare = () => {
    if (selectedLaptops.length >= 2) {
      setShowComparison(true)
    }
  }

  const clearComparison = () => {
    setSelectedLaptops([])
    setShowComparison(false)
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Hero Section */}
      <div className="mb-8 text-center relative overflow-hidden rounded-2xl bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500 p-8 backdrop-blur-lg">
        <div className="absolute inset-0 bg-black/20"></div>
        <div className="relative z-10">
          <div className="text-6xl mb-4 animate-bounce">💻</div>
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-3">
            Laptop Finder Pakistan
          </h1>
          <p className="text-white/90 text-lg">
            AI-powered recommendations for Pakistani students
          </p>
        </div>
      </div>

      {/* Comparison View */}
      {showComparison && (
        <ComparisonView
          laptops={selectedLaptops}
          onClose={clearComparison}
        />
      )}

      {/* Chat Container */}
      <div className="bg-white/10 backdrop-blur-md rounded-2xl shadow-2xl overflow-hidden border border-white/20">
        <div className="h-[600px] flex flex-col">
          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gradient-to-b from-gray-50 to-white">
            {messages.map((msg, idx) => (
              <div key={idx}>
                <MessageBubble message={msg} />
                {msg.recommendations && msg.recommendations.length > 0 && (
                  <div className="mt-4 space-y-3">
                    {msg.recommendations.map((laptop, i) => (
                      <LaptopCard
                        key={i}
                        laptop={laptop}
                        onSelect={handleLaptopSelect}
                        isSelected={selectedLaptops.some(l => l.id === laptop.id)}
                      />
                    ))}
                  </div>
                )}
              </div>
            ))}
            
            {loading && (
              <div className="flex justify-start items-center space-x-3">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white">
                  🤖
                </div>
                <div className="bg-white rounded-2xl px-6 py-3 shadow-lg">
                  <div className="flex space-x-2">
                    <div className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-purple-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-pink-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Quick Replies */}
          {!loading && messages.length <= 2 && (
            <QuickReplies onSelect={handleQuickReply} />
          )}

          {/* Comparison Bar */}
          {selectedLaptops.length > 0 && (
            <div className="bg-indigo-50 border-t border-indigo-200 px-6 py-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <span className="text-sm font-medium text-indigo-900">
                    {selectedLaptops.length} laptop{selectedLaptops.length > 1 ? 's' : ''} selected
                  </span>
                  {selectedLaptops.map(laptop => (
                    <span key={laptop.id} className="text-xs bg-indigo-200 text-indigo-800 px-2 py-1 rounded-full">
                      {laptop.brand}
                    </span>
                  ))}
                </div>
                <div className="flex space-x-2">
                  <button
                    onClick={clearComparison}
                    className="text-sm text-indigo-600 hover:text-indigo-800"
                  >
                    Clear
                  </button>
                  {selectedLaptops.length >= 2 && (
                    <button
                      onClick={handleCompare}
                      className="text-sm bg-indigo-600 text-white px-4 py-1 rounded-lg hover:bg-indigo-700"
                    >
                      Compare
                    </button>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Input Area */}
          <div className="border-t border-gray-200 p-4 bg-white">
            <div className="flex space-x-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && !loading && sendMessage()}
                placeholder="Ask about laptops, budget, or where to buy..."
                className="flex-1 border-2 border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition"
                disabled={loading}
              />
              <button
                onClick={() => sendMessage()}
                disabled={loading || !input.trim()}
                className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-6 py-3 rounded-xl hover:from-indigo-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition transform hover:scale-105 active:scale-95"
              >
                <span className="text-xl">📤</span>
              </button>
            </div>
            <p className="text-xs text-gray-500 mt-2 text-center">
              Powered by AI • Pakistani Market Data • Real-time Prices
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
