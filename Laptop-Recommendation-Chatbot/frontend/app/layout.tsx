import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Laptop Recommendation Chatbot',
  description: 'AI-powered laptop recommendations for Pakistani students',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
