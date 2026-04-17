import React from 'react'
import { Link } from 'react-router-dom'
import { CheckCircle } from 'lucide-react'
import type { Module } from '@/types'
import DynamicIcon from '@/components/ui/DynamicIcon'
import { progressBarClass } from '@/utils/progressColor'

interface Props {
  module: Module
  progressPercent?: number
}

const ModuleCard: React.FC<Props> = ({ module, progressPercent = 0 }) => {
  const clampedPercent = Math.min(100, Math.max(0, progressPercent))
  const isComplete = clampedPercent >= 100

  return (
    <Link
      to={`/curriculum/${module.slug}`}
      className={`block card-interactive p-4 relative ${isComplete ? 'card-complete' : ''}`}
    >
      {isComplete && (
        <div className="absolute top-3 right-3">
          <CheckCircle size={16} className="text-gold" />
        </div>
      )}
      {module.icon !== null && (
        <DynamicIcon
          name={module.icon}
          size={24}
          strokeWidth={1.5}
          className={isComplete ? 'text-amber drop-shadow-[0_0_8px_rgba(232,177,79,0.55)]' : 'text-gold'}
        />
      )}
      <h3 className="text-white font-semibold mt-2 pr-6">{module.title}</h3>
      <p className="text-muted text-sm mt-1 line-clamp-2">{module.description}</p>
      <div className="flex gap-4 mt-3">
        <span className="text-muted text-xs">{module.estimated_hours}h</span>
        <span className="text-gold text-xs">{module.xp_reward} XP</span>
        {clampedPercent > 0 && (
          <span className="text-xs" style={{ color: isComplete ? '#10b981' : '#C9A84C' }}>
            {Math.round(clampedPercent)}%
          </span>
        )}
      </div>
      <div className="h-1.5 bg-border rounded mt-3 overflow-hidden">
        <div
          className={`h-full transition-all duration-500 ${progressBarClass(clampedPercent)}`}
          style={{ width: `${clampedPercent}%` }}
        />
      </div>
    </Link>
  )
}

export default ModuleCard
