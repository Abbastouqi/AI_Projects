import { Message } from '@/types/chat'

interface MessageBubbleProps {
  message: Message
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} items-end space-x-2`}>
      {!isUser && (
        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white flex-shrink-0 shadow-lg">
          🤖
        </div>
      )}
      <div
        className={`max-w-[70%] rounded-2xl px-5 py-3 shadow-lg ${
          isUser
            ? 'bg-gradient-to-br from-indigo-600 to-purple-600 text-white'
            : 'bg-white text-gray-800 border border-gray-200'
        }`}
      >
        <p className="whitespace-pre-wrap text-sm leading-relaxed">{message.content}</p>
        <span className={`text-xs mt-1 block ${isUser ? 'text-indigo-100' : 'text-gray-400'}`}>
          {new Date(message.timestamp).toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit' 
          })}
        </span>
      </div>
      {isUser && (
        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-green-400 to-blue-500 flex items-center justify-center text-white flex-shrink-0 shadow-lg">
          👤
        </div>
      )}
    </div>
  )
}
