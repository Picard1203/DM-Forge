import React from 'react'
import type { QuizResult as QuizResultType } from '@/types'

interface Props {
  result: QuizResultType
}

const QuizResult: React.FC<Props> = ({ result }) => {
  return (
    <div className="bg-surface border border-border rounded-lg p-6 text-center space-y-2">
      <p className={`text-3xl font-bold ${result.passed ? 'text-gold' : 'text-primary'}`}>
        {result.score}%
      </p>
      <p className="text-white">{result.passed ? 'Passed!' : 'Not quite — try again'}</p>
      <p className="text-muted text-sm">
        {result.correct_count}/{result.total_count} correct · +{result.xp_awarded} XP
      </p>
    </div>
  )
}

export default QuizResult
