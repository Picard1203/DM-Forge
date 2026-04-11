import React from 'react'
import Navbar from '@/components/layout/Navbar'

const AchievementsPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-bg">
      <Navbar />
      <main className="max-w-5xl mx-auto px-6 py-10">
        <h1 className="text-white text-2xl font-bold mb-6">Achievements</h1>
        <p className="text-muted">Achievement gallery — coming soon</p>
      </main>
    </div>
  )
}

export default AchievementsPage
