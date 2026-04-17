import React from 'react'
import type { QuizQuestion } from '@/types'

interface Props {
  question: QuizQuestion
  selectedIndex: number | null
  onSelect: (index: number) => void
}

const QuestionCard: React.FC<Props> = ({ question, selectedIndex, onSelect }) => {
  return (
    <div className="card-surface p-6 space-y-4">
      <p className="text-white font-medium">{question.question_text}</p>
      <ul className="space-y-2">
        {question.options.map((option, i) => (
          <li key={i}>
            <button
              onClick={() => onSelect(i)}
              className={`w-full text-left px-4 py-2 rounded border text-sm transition-colors ${
                selectedIndex === i
                  ? 'border-primary bg-primary/10 text-white'
                  : 'border-border hover:border-primary/50 text-muted'
              }`}
            >
              {option}
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default QuestionCard
