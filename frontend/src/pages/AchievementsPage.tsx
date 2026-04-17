import React, { useEffect, useState } from 'react'
import Navbar from '@/components/layout/Navbar'
import AchievementGrid from '@/components/achievements/AchievementGrid'
import * as achievementsApi from '@/api/achievements'
import type { AchievementResponse, UserAchievementResponse } from '@/types'

const AchievementsPage: React.FC = () => {
  const [all, setAll] = useState<AchievementResponse[]>([])
  const [mine, setMine] = useState<UserAchievementResponse[]>([])
  const [isLoading, setIsLoading] = useState<boolean>(true)

  useEffect(() => {
    Promise.all([
      achievementsApi.listAchievements(),
      achievementsApi.getMyAchievements(),
    ]).then(([allData, mineData]) => {
      setAll(allData)
      setMine(mineData)
      setIsLoading(false)
    }).catch(() => {
      setIsLoading(false)
    })
  }, [])

  const earnedIds = new Set(mine.map((ua) => ua.id))
  const earnedCount = earnedIds.size

  return (
    <div className="min-h-screen bg-bg">
      <Navbar />
      <main className="max-w-5xl mx-auto px-6 py-10">
        <div className="flex items-baseline gap-4 mb-6">
          <h1 className="font-display text-3xl md:text-4xl font-bold tracking-wide text-white">Achievements</h1>
          {!isLoading && (
            <span className="text-muted text-sm">
              {earnedCount} / {all.length} earned
            </span>
          )}
        </div>

        {isLoading && (
          <p className="text-muted text-sm">Loading achievements...</p>
        )}

        {!isLoading && all.length === 0 && (
          <p className="text-muted text-sm">No achievements found.</p>
        )}

        {!isLoading && all.length > 0 && (
          <AchievementGrid achievements={all} earnedIds={earnedIds} />
        )}
      </main>
    </div>
  )
}

export default AchievementsPage
