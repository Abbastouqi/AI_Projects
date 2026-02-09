interface QuickRepliesProps {
  onSelect: (text: string) => void
}

export default function QuickReplies({ onSelect }: QuickRepliesProps) {
  const quickReplies = [
    { emoji: '📚', text: 'FSC Student', message: 'I am an FSC student' },
    { emoji: '💻', text: 'Programming', message: 'I need a laptop for programming' },
    { emoji: '💰', text: '80k Budget', message: 'My budget is around 80,000 PKR' },
    { emoji: '🎮', text: 'Gaming', message: 'I want a gaming laptop' },
    { emoji: '📊', text: 'Office Work', message: 'I need it for office work' },
    { emoji: '🔧', text: 'Engineering', message: 'I am an engineering student' },
  ]

  return (
    <div className="px-6 py-4 bg-gradient-to-r from-indigo-50 to-purple-50 border-t border-gray-200">
      <p className="text-xs text-gray-600 mb-3 font-medium">Quick Replies:</p>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
        {quickReplies.map((reply, idx) => (
          <button
            key={idx}
            onClick={() => onSelect(reply.message)}
            className="flex items-center space-x-2 bg-white hover:bg-indigo-50 border-2 border-gray-200 hover:border-indigo-300 rounded-xl px-4 py-2 text-sm font-medium text-gray-700 hover:text-indigo-700 transition-all duration-200 transform hover:scale-105"
          >
            <span className="text-lg">{reply.emoji}</span>
            <span>{reply.text}</span>
          </button>
        ))}
      </div>
    </div>
  )
}
