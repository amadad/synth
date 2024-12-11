'use client'

import { useState, useEffect } from 'react'
import { api } from '@/app/lib/api'

type Environment = {
  id: string
  name: string
}

export function EnvironmentSelect() {
  const [selected, setSelected] = useState<string>('default')
  const [environments, setEnvironments] = useState<Environment[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function loadEnvironments() {
      try {
        const data = await api.getEnvironments()
        setEnvironments(data)
        if (data.length > 0 && !selected) {
          setSelected(data[0].id)
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load environments')
      } finally {
        setLoading(false)
      }
    }

    loadEnvironments()
  }, [])

  if (loading) return <div>Loading...</div>
  if (error) return <div className="text-red-500">Error: {error}</div>

  return (
    <select
      value={selected}
      onChange={(e) => setSelected(e.target.value)}
      className="px-3 py-1 border rounded-md bg-white"
    >
      {environments.map((env) => (
        <option key={env.id} value={env.id}>
          {env.name}
        </option>
      ))}
    </select>
  )
} 