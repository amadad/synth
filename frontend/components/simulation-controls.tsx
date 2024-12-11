'use client'

import { useState } from 'react'
import { api } from '@/app/lib/api'

export function SimulationControls() {
  const [isRunning, setIsRunning] = useState(false)
  const [stepCount, setStepCount] = useState(1)
  const [error, setError] = useState<string | null>(null)

  const handleStart = async () => {
    try {
      await api.startSimulation()
      setIsRunning(true)
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to start simulation')
    }
  }

  const handlePause = async () => {
    try {
      await api.pauseSimulation()
      setIsRunning(false)
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to pause simulation')
    }
  }

  const handleStep = async () => {
    try {
      await api.stepSimulation(stepCount)
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to step simulation')
    }
  }

  return (
    <div className="flex flex-col gap-2">
      <div className="flex items-center gap-2">
        {!isRunning ? (
          <button
            onClick={handleStart}
            className="px-3 py-1 bg-blue-500 text-white rounded-md hover:bg-blue-600"
          >
            Start
          </button>
        ) : (
          <button
            onClick={handlePause}
            className="px-3 py-1 bg-yellow-500 text-white rounded-md hover:bg-yellow-600"
          >
            Pause
          </button>
        )}
        <button
          onClick={handleStep}
          className="px-3 py-1 bg-gray-500 text-white rounded-md hover:bg-gray-600"
        >
          Step
        </button>
        <input
          type="number"
          min="1"
          value={stepCount}
          onChange={(e) => setStepCount(parseInt(e.target.value) || 1)}
          className="w-16 px-2 py-1 border rounded-md"
        />
      </div>
      {error && <div className="text-red-500 text-sm">{error}</div>}
    </div>
  )
} 