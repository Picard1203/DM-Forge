import React from 'react'

interface Props {
  onSelect: (quality: number) => void
  disabled: boolean
}

const LABELS: Record<number, string> = {
  0: 'Blackout',
  1: 'Wrong',
  2: 'Hard',
  3: 'OK',
  4: 'Good',
  5: 'Perfect',
}

const QualityButtons: React.FC<Props> = ({ onSelect, disabled }) => {
  return (
    <div className="flex gap-2 justify-center">
      {[0, 1, 2, 3, 4, 5].map((q) => (
        <button
          key={q}
          onClick={() => onSelect(q)}
          disabled={disabled}
          className="px-3 py-2 rounded-lg border border-white/10 bg-card-surface text-sm text-muted hover:border-amber/50 hover:text-white disabled:opacity-40 transition-colors"
        >
          {LABELS[q]}
        </button>
      ))}
    </div>
  )
}

export default QualityButtons
