import React from 'react'
import { Flame } from 'lucide-react'
import { useTranslation } from 'react-i18next'

interface Props {
  currentStreak: number
  longestStreak: number
}

const StreakWidget: React.FC<Props> = ({ currentStreak, longestStreak }) => {
  const { t } = useTranslation()

  return (
    <div className="card-surface p-4">
      <div className="flex items-center gap-2 mb-1">
        <Flame size={14} className="text-amber" strokeWidth={1.5} />
        <p className="text-muted text-xs uppercase tracking-wider">Streak</p>
      </div>
      <p className="text-gold text-2xl font-bold mt-1">
        {t('dashboard.streak', { count: currentStreak })}
      </p>
      <p className="text-muted text-xs mt-1">
        {t('dashboard.streak_best', { count: longestStreak })}
      </p>
    </div>
  )
}

export default StreakWidget
