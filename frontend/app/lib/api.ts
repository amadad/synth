const API_BASE = 'http://localhost:8000'

export async function fetchApi(endpoint: string, options: RequestInit = {}) {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  })

  if (!response.ok) {
    throw new Error(`API Error: ${response.statusText}`)
  }

  return response.json()
}

// API endpoints
export const api = {
  // Environment endpoints
  getEnvironments: () => fetchApi('/environments'),
  getEnvironmentState: () => fetchApi('/environment/state'),

  // Simulation control
  startSimulation: (environmentId?: string) => 
    fetchApi('/simulation/start', {
      method: 'POST',
      body: JSON.stringify({ environment_id: environmentId }),
    }),
  pauseSimulation: () => fetchApi('/simulation/pause', { method: 'POST' }),
  resumeSimulation: () => fetchApi('/simulation/resume', { method: 'POST' }),
  stopSimulation: () => fetchApi('/simulation/stop', { method: 'POST' }),
  stepSimulation: (steps: number) => 
    fetchApi('/simulation/step', {
      method: 'POST',
      body: JSON.stringify({ body: steps }),
    }),

  // Data endpoints
  getEvents: () => fetchApi('/events'),
  getStory: () => fetchApi('/story'),
  getAgents: () => fetchApi('/agents'),
} 