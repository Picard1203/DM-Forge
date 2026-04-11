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
      className="bg-surface border border-border rounded-lg p-8 text-center cursor-pointer min-h-48 flex items-center justify-center hover:border-primary/50 transition-colors"
    >
      <p className="text-white text-lg">{flipped ? card.back : card.front}</p>
    </div>
  )
}

export default FlashCard
