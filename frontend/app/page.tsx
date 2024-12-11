'use client'

import { useState } from 'react'
import { TimelineView } from '@/components/timeline-view'
import { StoryView } from '@/components/story-view'
import { EnvironmentView } from '@/components/environment-view'

export default function Page() {
  const [activeTab, setActiveTab] = useState('timeline')

  return (
    <div className="w-full h-full flex flex-col">
      <div className="border-b">
        <nav className="flex" aria-label="Tabs">
          {['Timeline', 'Story', 'Environment'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab.toLowerCase())}
              className={`px-4 py-2 text-sm font-medium ${
                activeTab === tab.toLowerCase()
                  ? 'border-b-2 border-blue-500 text-blue-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              {tab}
            </button>
          ))}
        </nav>
      </div>
      <div className="flex-1 pt-4">
        {activeTab === 'timeline' && <TimelineView />}
        {activeTab === 'story' && <StoryView />}
        {activeTab === 'environment' && <EnvironmentView />}
      </div>
    </div>
  )
}
