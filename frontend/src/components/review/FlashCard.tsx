import React, { useState } from 'react'
import type { ReviewCard } from '@/types'

interface Props {
  card: ReviewCard
}

const FlashCard: React.FC<Props> = ({ card }) => {
  const [flipped, setFlipped] = useState(false)

  return (
    <div
      onClick={() => setFlipped(!flipped)}
      className="card-interactive p-8 text-center min-h-56 flex flex-col items-center justify-center gap-3"
    >
      <p className="text-muted text-xs uppercase tracking-widest">
        {flipped ? 'Answer' : 'Question'}
      </p>
      <p className="text-white text-lg leading-relaxed">{flipped ? card.back : card.front}</p>
      {!flipped && (
        <p className="text-muted/60 text-xs mt-2">click to flip</p>
      )}
    </div>
  )
}

export default FlashCard
