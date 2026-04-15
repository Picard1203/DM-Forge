import React from 'react'

const XP_THRESHOLDS: number[] = [
  0, 300, 900, 2100, 6500, 14000, 28000, 48000,
  64000, 85000, 110000, 140000, 165000, 195000, 230000,
  270000, 310000, 330000, 345000, 355000,
]

interface Props {
  xp: number
  level: number
  title: string
}

const XPBar: React.FC<Props> = ({ xp, level, title }) => {
  const currentThreshold = XP_THRESHOLDS[level - 1] ?? 0
  const nextThreshold = XP_THRESHOLDS[level] ?? XP_THRESHOLDS[XP_THRESHOLDS.length - 1]
  const isMaxLevel = level >= XP_THRESHOLDS.length

  const progressPercent = isMaxLevel
    ? 100
    : Math.min(100, ((xp - currentThreshold) / (nextThreshold - currentThreshold)) * 100)

  return (
    <div className="bg-surface border border-border rounded-lg p-4">
      <div className="flex items-center justify-between mb-2">
        <div>
          <span className="text-gold font-bold text-lg">Level {level}</span>
          <span className="text-muted text-sm ml-2">{title}</span>
        </div>
        <span className="text-white text-sm font-medium">{xp.toLocaleString()} XP</span>
      </div>
      <div className="w-full bg-bg rounded-full h-2">
        <div
          className="bg-gold h-2 rounded-full transition-all duration-500"
          style={{ width: `${progressPercent}%` }}
        />
      </div>
      {!isMaxLevel && (
        <p className="text-muted text-xs mt-1">
          {(nextThreshold - xp).toLocaleString()} XP to level {level + 1}
        </p>
      )}
    </div>
  )
}

export default XPBar
