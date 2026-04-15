import React from 'react'
import type { AchievementResponse } from '@/types'

interface Props {
  achievement: AchievementResponse
  earned: boolean
}

const AchievementBadge: React.FC<Props> = ({ achievement, earned }) => {
  return (
    <div className={`border rounded-lg p-4 text-center ${earned ? 'border-gold bg-gold/5' : 'border-border opacity-40'}`}>
      <p className="text-2xl mb-2">{achievement.icon}</p>
      <p className="text-white text-sm font-semibold">{achievement.title}</p>
      <p className="text-muted text-xs mt-1">{achievement.description}</p>
      <p className="text-gold text-xs mt-2">+{achievement.xp_reward} XP</p>
    </div>
  )
}

export default AchievementBadge
