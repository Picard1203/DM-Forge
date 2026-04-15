import React from 'react'
import type { AchievementResponse } from '@/types'
import AchievementBadge from './AchievementBadge'

interface Props {
  achievements: AchievementResponse[]
  earnedIds: Set<string>
}

const AchievementGrid: React.FC<Props> = ({ achievements, earnedIds }) => {
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {achievements.map((a) => (
        <AchievementBadge key={a.id} achievement={a} earned={earnedIds.has(a.id)} />
      ))}
    </div>
  )
}

export default AchievementGrid
