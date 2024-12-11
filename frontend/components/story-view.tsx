'use client'

import { useState, useEffect } from 'react'
import { api } from '@/app/lib/api'

type StorySegment = {
  id: string
  content: string
  timestamp: string
}

const POLL_INTERVAL = 5000 // Poll every 5 seconds

export function StoryView() {
  const [story, setStory] = useState<StorySegment[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let mounted = true
    let pollInterval: NodeJS.Timeout

    async function fetchStory() {
      try {
        const data = await api.getStory()
        if (mounted) {
          setStory(Array.isArray(data) ? data : [data])
          setError(null)
        }
      } catch (err) {
        if (mounted) {
          setError(err instanceof Error ? err.message : 'Failed to load story')
        }
      } finally {
        if (mounted) {
          setLoading(false)
        }
      }
    }

    // Initial fetch
    fetchStory()

    // Set up polling
    pollInterval = setInterval(fetchStory, POLL_INTERVAL)

    return () => {
      mounted = false
      clearInterval(pollInterval)
    }
  }, [])

  if (loading) return <div>Loading story...</div>
  if (error) return <div className="text-red-500">Error: {error}</div>
  if (story.length === 0) return <div>No story content yet</div>

  return (
    <div className="max-w-2xl mx-auto">
      <div className="prose">
        {story.map((segment) => (
          <div key={segment.id} className="mb-6">
            <p className="text-gray-800 leading-relaxed">{segment.content}</p>
            <div className="text-sm text-gray-500 mt-2">{segment.timestamp}</div>
          </div>
        ))}
      </div>
    </div>
  )
} 