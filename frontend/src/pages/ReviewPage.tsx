import React, { useEffect, useState } from 'react'
import Navbar from '@/components/layout/Navbar'
import FlashCard from '@/components/review/FlashCard'
import QualityButtons from '@/components/review/QualityButtons'
import * as reviewApi from '@/api/review'
import type { ReviewCard } from '@/types'

const ReviewPage: React.FC = () => {
  const [cards, setCards] = useState<ReviewCard[]>([])
  const [currentIndex, setCurrentIndex] = useState<number>(0)
  const [isLoading, setIsLoading] = useState<boolean>(true)
  const [isFlipped, setIsFlipped] = useState<boolean>(false)

  useEffect(() => {
    reviewApi.getDueCards().then((data) => {
      setCards(data)
      setIsLoading(false)
    }).catch(() => {
      setIsLoading(false)
    })
  }, [])

  const handleFlip = () => {
    setIsFlipped(true)
  }

  const handleQuality = (quality: number) => {
    const card = cards[currentIndex]
    if (card === undefined) return
    setIsFlipped(false)
    setCurrentIndex((prev) => prev + 1)
    reviewApi.submitReview(card.id, quality).catch(() => {})
  }

  const currentCard = cards[currentIndex]
  const isDone = !isLoading && currentIndex >= cards.length
  const deckBehind = cards.length > 0 ? Math.min(cards.length - currentIndex - 1, 2) : 0
  const progressPercent = cards.length > 0 ? (currentIndex / cards.length) * 100 : 0

  return (
    <div className="min-h-screen bg-bg">
      <Navbar />
      <main className="max-w-2xl mx-auto px-6 py-10">
        <div className="flex items-center justify-between mb-4">
          <h1 className="font-display text-3xl md:text-4xl font-bold tracking-wide text-white">
            Spaced Review
          </h1>
        </div>

        {cards.length > 0 && !isDone && (
          <div className="mb-6">
            <div className="flex justify-between text-xs text-muted mb-1">
              <span>Progress</span>
              <span>{currentIndex + 1} / {cards.length}</span>
            </div>
            <div className="w-full bg-border rounded-full h-1.5 overflow-hidden">
              <div
                className="h-1.5 bg-gold rounded-full transition-all duration-300"
                style={{ width: `${progressPercent}%` }}
              />
            </div>
          </div>
        )}

        {isLoading && (
          <p className="text-muted text-sm">Loading cards...</p>
        )}

        {isDone && (
          <div className="card-surface p-8 text-center">
            <p className="text-gold text-2xl font-bold mb-2">All done!</p>
            <p className="text-muted text-sm">No more cards due for review right now.</p>
          </div>
        )}

        {!isLoading && !isDone && currentCard !== undefined && (
          <div className="space-y-6">
            <div className="relative" onClick={!isFlipped ? handleFlip : undefined}>
              {deckBehind >= 2 && (
                <div className="absolute inset-0 card-surface opacity-30 -translate-y-3 translate-x-2 -z-20 rounded-xl" />
              )}
              {deckBehind >= 1 && (
                <div className="absolute inset-0 card-surface opacity-50 -translate-y-1.5 translate-x-1 -z-10 rounded-xl" />
              )}
              <FlashCard key={currentCard.id} card={currentCard} />
            </div>

            {!isFlipped && (
              <p className="text-muted text-xs text-center">Click the card to reveal the answer</p>
            )}

            {isFlipped && (
              <div className="space-y-3">
                <p className="text-muted text-xs text-center">How well did you know this?</p>
                <QualityButtons onSelect={handleQuality} disabled={false} />
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  )
}

export default ReviewPage
