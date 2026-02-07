import { Laptop } from '@/types/chat'

interface LaptopCardProps {
  laptop: Laptop
  onSelect?: (laptop: Laptop) => void
  isSelected?: boolean
}

export default function LaptopCard({ laptop, onSelect, isSelected }: LaptopCardProps) {
  return (
    <div className={`border-2 rounded-xl p-5 bg-gradient-to-br from-white to-gray-50 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 ${
      isSelected ? 'border-indigo-500 ring-2 ring-indigo-200' : 'border-gray-200'
    }`}>
      <div className="flex justify-between items-start mb-3">
        <div className="flex-1">
          <h3 className="font-bold text-lg text-gray-800 mb-1">{laptop.name}</h3>
          <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
            {laptop.category}
          </span>
        </div>
        <div className="text-right">
          <div className="bg-gradient-to-r from-green-500 to-emerald-600 text-white px-4 py-2 rounded-xl shadow-md">
            <div className="text-xs font-medium">PKR</div>
            <div className="text-lg font-bold">{laptop.price_pkr.toLocaleString()}</div>
          </div>
        </div>
      </div>
      
      <div className="grid grid-cols-2 gap-3 text-sm text-gray-700 mb-4 bg-gray-50 p-3 rounded-lg">
        <div className="flex items-center space-x-2">
          <span className="text-indigo-600">⚡</span>
          <div>
            <div className="text-xs text-gray-500">Processor</div>
            <div className="font-medium">{laptop.processor.split('(')[0].trim()}</div>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <span className="text-purple-600">💾</span>
          <div>
            <div className="text-xs text-gray-500">RAM</div>
            <div className="font-medium">{laptop.ram}</div>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <span className="text-blue-600">💿</span>
          <div>
            <div className="text-xs text-gray-500">Storage</div>
            <div className="font-medium">{laptop.storage}</div>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <span className="text-pink-600">🖥️</span>
          <div>
            <div className="text-xs text-gray-500">Display</div>
            <div className="font-medium">{laptop.display}</div>
          </div>
        </div>
      </div>

      <div className="flex space-x-2">
        {laptop.url && (
          <a
            href={laptop.url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex-1 text-center bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium py-2 px-4 rounded-lg transition transform hover:scale-105"
          >
            View Details →
          </a>
        )}
        {onSelect && (
          <button
            onClick={() => onSelect(laptop)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
              isSelected
                ? 'bg-indigo-600 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            {isSelected ? '✓ Selected' : 'Compare'}
          </button>
        )}
      </div>
    </div>
  )
}
