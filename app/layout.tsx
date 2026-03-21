import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Peach Agents - Trading Platform',
  description: 'Automated trading system with AI-powered market intelligence',
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
