import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'PEACH&AGENTS - Trading Platform',
  description: 'Intelligent trading bot management with Alpaca integration',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-slate-950 text-white">{children}</body>
    </html>
  )
}
