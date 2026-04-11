import React from 'react'
import { Link } from 'react-router-dom'
import type { Module } from '@/types'

interface Props {
  module: Module
}

const ModuleCard: React.FC<Props> = ({ module }) => {
  return (
    <Link
      to={`/curriculum/${module.slug}`}
      className="block bg-surface border border-border rounded-lg p-4 hover:border-primary/50 transition-colors"
    >
      {module.icon !== null && (
        <p className="text-gold text-xl">{module.icon}</p>
      )}
      <h3 className="text-white font-semibold mt-2">{module.title}</h3>
      <p className="text-muted text-sm mt-1 line-clamp-2">{module.description}</p>
      <div className="flex gap-4 mt-3">
        <span className="text-muted text-xs">{module.estimated_hours}h</span>
        <span className="text-gold text-xs">{module.xp_reward} XP</span>
      </div>
      <div className="h-1.5 bg-border rounded mt-3 overflow-hidden">
        <div className="h-full bg-primary" style={{ width: '0%' }} />
      </div>
    </Link>
  )
}

export default ModuleCard
