import React from 'react'

interface Props {
  currentStreak: number
  longestStreak: number
}

const StreakWidget: React.FC<Props> = ({ currentStreak, longestStreak }) => {
  return (
    <div className="bg-surface border border-border rounded-lg p-4">
      <p className="text-muted text-xs uppercase tracking-wider">Streak</p>
      <p className="text-gold text-2xl font-bold mt-1">{currentStreak} days</p>
      <p className="text-muted text-xs mt-1">Best: {longestStreak} days</p>
    </div>
  )
}

export default StreakWidget
