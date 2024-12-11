import './globals.css'
import { ReactNode } from 'react'
import { Inter } from 'next/font/google'
import { EnvironmentSelect } from '@/components/environment-select'
import { SimulationControls } from '@/components/simulation-controls'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'TinyTroupe Simulation',
  description: 'Frontend UI for TinyTroupe simulations'
}

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className={`${inter.className} min-h-screen flex flex-col`}>
        <header className="border-b p-4 flex items-center justify-between">
          <div className="font-bold text-xl">TinyTroupe Simulation</div>
          <div className="flex gap-4">
            <EnvironmentSelect />
            <SimulationControls />
          </div>
        </header>
        <div className="flex flex-1">
          <aside className="w-64 border-r p-4 overflow-auto">
            <div className="font-semibold mb-2">Agents</div>
            <div id="agent-list">
              {/* Agent cards will go here */}
            </div>
          </aside>
          <main className="flex-1 p-4 overflow-auto">
            {children}
          </main>
        </div>
      </body>
    </html>
  )
}
