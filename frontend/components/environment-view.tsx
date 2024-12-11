'use client'

import { useState, useEffect } from 'react'
import { api } from '@/app/lib/api'

type EnvironmentState = {
  currentTime: string
  location: string
  agents: {
    id: string
    name: string
    location: string
    status: string
  }[]
  objects: {
    id: string
    name: string
    location: string
  }[]
}

const POLL_INTERVAL = 2000 // Poll every 2 seconds

export function EnvironmentView() {
  const [state, setState] = useState<EnvironmentState | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let mounted = true
    let pollInterval: NodeJS.Timeout

    async function fetchState() {
      try {
        const data = await api.getEnvironmentState()
        if (mounted) {
          setState(data)
          setError(null)
        }
      } catch (err) {
        if (mounted) {
          setError(err instanceof Error ? err.message : 'Failed to load environment state')
        }
      } finally {
        if (mounted) {
          setLoading(false)
        }
      }
    }

    // Initial fetch
    fetchState()

    // Set up polling
    pollInterval = setInterval(fetchState, POLL_INTERVAL)

    return () => {
      mounted = false
      clearInterval(pollInterval)
    }
  }, [])

  if (loading) return <div>Loading environment state...</div>
  if (error) return <div className="text-red-500">Error: {error}</div>
  if (!state) return <div>No environment state available</div>

  return (
    <div className="space-y-6">
      <div className="bg-white p-4 rounded-lg border">
        <h2 className="text-lg font-semibold mb-2">Environment Info</h2>
        <div>Current Time: {state.currentTime}</div>
        <div>Location: {state.location}</div>
      </div>

      <div className="bg-white p-4 rounded-lg border">
        <h2 className="text-lg font-semibold mb-2">Agents</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {state.agents.map((agent) => (
            <div key={agent.id} className="p-3 border rounded">
              <div className="font-medium">{agent.name}</div>
              <div>Location: {agent.location}</div>
              <div>Status: {agent.status}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white p-4 rounded-lg border">
        <h2 className="text-lg font-semibold mb-2">Objects</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {state.objects.map((object) => (
            <div key={object.id} className="p-3 border rounded">
              <div className="font-medium">{object.name}</div>
              <div>Location: {object.location}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
} 