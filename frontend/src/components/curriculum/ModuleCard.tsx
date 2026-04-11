import React from 'react'
import type { Module } from '@/types'

interface Props {
  module: Module
}

const ModuleCard: React.FC<Props> = ({ module }) => {
  return (
    <div className="bg-surface border border-border rounded-lg p-4 hover:border-primary/50 transition-colors cursor-pointer">
      <p className="text-gold text-xl">{module.icon}</p>
      <h3 className="text-white font-semibold mt-2">{module.title}</h3>
      <p className="text-muted text-sm mt-1 line-clamp-2">{module.description}</p>
      <p className="text-muted text-xs mt-3">{module.estimated_minutes} min</p>
    </div>
  )
}

export default ModuleCard
