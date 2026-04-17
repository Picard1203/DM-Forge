import React from 'react'
import type { QuizResult as QuizResultType } from '@/types'

interface Props {
  result: QuizResultType
}

const QuizResult: React.FC<Props> = ({ result }) => {
  const correctCount = result.question_results.filter((qr) => qr.correct).length
  const totalCount = result.question_results.length

  return (
    <div className="card-surface p-6 space-y-4">
      <div className="text-center space-y-2">
        <p className={`text-3xl font-bold ${result.passed ? 'text-gold' : 'text-primary'}`}>
          {Math.round(result.score * 100)}%
        </p>
        <p className="text-white">{result.passed ? 'Passed!' : 'Not quite — try again'}</p>
        <p className="text-muted text-sm">
          {correctCount}/{totalCount} correct · +{result.xp_earned} XP
        </p>
      </div>
      {result.question_results.length > 0 && (
        <div className="space-y-2">
          {result.question_results.map((qr) => (
            <div
              key={qr.question_index}
              className={`rounded p-3 text-sm border ${qr.correct ? 'border-green-500/30 bg-green-500/5' : 'border-red-500/30 bg-red-500/5'}`}
            >
              <p className={`font-medium ${qr.correct ? 'text-green-400' : 'text-red-400'}`}>
                {qr.correct ? '✓ Correct' : '✗ Incorrect'}
              </p>
              <p className="text-muted mt-1">{qr.explanation}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default QuizResult
