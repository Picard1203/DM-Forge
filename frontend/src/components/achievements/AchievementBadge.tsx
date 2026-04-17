import React from 'react'
import type { AchievementResponse } from '@/types'
import DynamicIcon from '@/components/ui/DynamicIcon'

interface Props {
  achievement: AchievementResponse
  earned: boolean
}

const AchievementBadge: React.FC<Props> = ({ achievement, earned }) => {
  return (
    <div className={`card-surface p-4 text-center relative ${earned ? 'card-complete' : 'opacity-50'}`}>
      <div className="flex justify-center mb-3">
        <div className={`p-2 rounded-full ${earned ? 'bg-gold/10 text-gold' : 'bg-border/30 text-muted'}`}>
          <DynamicIcon name={achievement.icon} size={28} strokeWidth={1.5} />
        </div>
      </div>
      <p className="text-white text-sm font-semibold leading-snug">{achievement.title}</p>
      <p className="text-white/70 text-xs mt-1 leading-relaxed">{achievement.description}</p>
      <span className="inline-flex items-center mt-2 bg-amber/10 border border-amber/40 text-amber px-2 py-0.5 rounded-full text-xs font-medium">
        +{achievement.xp_reward} XP
      </span>
    </div>
  )
}

export default AchievementBadge
