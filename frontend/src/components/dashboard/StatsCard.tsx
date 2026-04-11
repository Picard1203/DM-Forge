import React from 'react'

interface Props {
  label: string
  value: string | number
}

const StatsCard: React.FC<Props> = ({ label, value }) => {
  return (
    <div className="bg-surface border border-border rounded-lg p-4">
      <p className="text-muted text-xs uppercase tracking-wider">{label}</p>
      <p className="text-white text-2xl font-bold mt-1">{value}</p>
    </div>
  )
}

export default StatsCard
