'use client'

import { useState, useEffect } from 'react'
import { api } from '@/app/lib/api'

type TimelineEvent = {
  id: string
  timestamp: string
  agent: string
  action: string
  description: string
}

const POLL_INTERVAL = 2000 // Poll every 2 seconds

export function TimelineView() {
  const [events, setEvents] = useState<TimelineEvent[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let mounted = true
    let pollInterval: NodeJS.Timeout

    async function fetchEvents() {
      try {
        const data = await api.getEvents()
        if (mounted) {
          setEvents(data)
          setError(null)
        }
      } catch (err) {
        if (mounted) {
          setError(err instanceof Error ? err.message : 'Failed to load events')
        }
      } finally {
        if (mounted) {
          setLoading(false)
        }
      }
    }

    // Initial fetch
    fetchEvents()

    // Set up polling
    pollInterval = setInterval(fetchEvents, POLL_INTERVAL)

    return () => {
      mounted = false
      clearInterval(pollInterval)
    }
  }, [])

  if (loading) return <div>Loading events...</div>
  if (error) return <div className="text-red-500">Error: {error}</div>
  if (events.length === 0) return <div>No events yet</div>

  return (
    <div className="space-y-4">
      {events.map((event) => (
        <div
          key={event.id}
          className="p-4 border rounded-lg hover:bg-gray-50"
        >
          <div className="flex justify-between items-start">
            <div className="font-medium">{event.agent}</div>
            <div className="text-sm text-gray-500">{event.timestamp}</div>
          </div>
          <div className="mt-1">
            <span className="text-blue-600">{event.action}:</span>{' '}
            {event.description}
          </div>
        </div>
      ))}
    </div>
  )
} 