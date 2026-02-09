import { Laptop } from '@/types/chat'

interface ComparisonViewProps {
  laptops: Laptop[]
  onClose: () => void
}

export default function ComparisonView({ laptops, onClose }: ComparisonViewProps) {
  const specs = [
    { key: 'processor', label: 'Processor', icon: '⚡' },
    { key: 'ram', label: 'RAM', icon: '💾' },
    { key: 'storage', label: 'Storage', icon: '💿' },
    { key: 'display', label: 'Display', icon: '🖥️' },
    { key: 'graphics', label: 'Graphics', icon: '🎮' },
    { key: 'price_pkr', label: 'Price', icon: '💰' },
  ]

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl max-w-6xl w-full max-h-[90vh] overflow-auto">
        {/* Header */}
        <div className="sticky top-0 bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-6 flex justify-between items-center">
          <div>
            <h2 className="text-2xl font-bold">Laptop Comparison</h2>
            <p className="text-indigo-100 text-sm">Compare specs side-by-side</p>
          </div>
          <button
            onClick={onClose}
            className="bg-white/20 hover:bg-white/30 rounded-full p-2 transition"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Comparison Table */}
        <div className="p-6">
          <div className="grid gap-4" style={{ gridTemplateColumns: `200px repeat(${laptops.length}, 1fr)` }}>
            {/* Header Row */}
            <div className="font-bold text-gray-700"></div>
            {laptops.map((laptop, idx) => (
              <div key={idx} className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl p-4 border-2 border-indigo-200">
                <h3 className="font-bold text-lg text-gray-800 mb-2">{laptop.brand}</h3>
                <p className="text-sm text-gray-600">{laptop.model || laptop.name}</p>
              </div>
            ))}

            {/* Spec Rows */}
            {specs.map((spec) => (
              <>
                <div className="flex items-center space-x-2 font-semibold text-gray-700 py-3 border-b border-gray-200">
                  <span className="text-xl">{spec.icon}</span>
                  <span>{spec.label}</span>
                </div>
                {laptops.map((laptop, idx) => (
                  <div key={idx} className="py-3 border-b border-gray-200">
                    {spec.key === 'price_pkr' ? (
                      <div className="bg-green-100 text-green-800 font-bold px-3 py-2 rounded-lg inline-block">
                        PKR {laptop[spec.key].toLocaleString()}
                      </div>
                    ) : (
                      <span className="text-gray-700">{laptop[spec.key as keyof Laptop]}</span>
                    )}
                  </div>
                ))}
              </>
            ))}

            {/* Category Row */}
            <div className="flex items-center space-x-2 font-semibold text-gray-700 py-3">
              <span className="text-xl">🎯</span>
              <span>Best For</span>
            </div>
            {laptops.map((laptop, idx) => (
              <div key={idx} className="py-3">
                <span className="text-sm bg-indigo-100 text-indigo-800 px-3 py-1 rounded-full">
                  {laptop.category}
                </span>
              </div>
            ))}

            {/* Action Row */}
            <div></div>
            {laptops.map((laptop, idx) => (
              <div key={idx} className="py-3">
                {laptop.url && (
                  <a
                    href={laptop.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block text-center bg-indigo-600 hover:bg-indigo-700 text-white font-medium py-2 px-4 rounded-lg transition"
                  >
                    View Details
                  </a>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Winner Badge */}
        <div className="bg-gradient-to-r from-yellow-50 to-orange-50 border-t border-yellow-200 p-6">
          <div className="flex items-center space-x-3">
            <span className="text-4xl">🏆</span>
            <div>
              <h3 className="font-bold text-gray-800">Best Value</h3>
              <p className="text-sm text-gray-600">
                {laptops.reduce((best, laptop) => 
                  (laptop.price_pkr < best.price_pkr) ? laptop : best
                ).brand} offers the lowest price at PKR {
                  laptops.reduce((best, laptop) => 
                    (laptop.price_pkr < best.price_pkr) ? laptop : best
                  ).price_pkr.toLocaleString()
                }
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
