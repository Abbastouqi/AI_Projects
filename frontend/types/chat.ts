export interface Message {
  role: 'user' | 'assistant'
  content: string
  recommendations?: Laptop[]
  timestamp: string
}

export interface Laptop {
  id: number
  name: string
  brand: string
  model?: string
  processor: string
  ram: string
  storage: string
  display: string
  graphics: string
  price_pkr: number
  category: string
  url?: string
  image?: string
}

export interface ChatSession {
  session_id: string
  conversation_history: Message[]
  preferences: UserPreferences
  created_at: string
}

export interface UserPreferences {
  student_type?: string
  major?: string
  use_case?: string[]
  budget_min?: number
  budget_max?: number
  brand_pref?: string[]
}
