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
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false)

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

  const handleQuality = async (quality: number) => {
    const card = cards[currentIndex]
    if (card === undefined) return
    setIsSubmitting(true)
    try {
      await reviewApi.submitReview(card.id, quality)
    } catch {
      // ignore
    } finally {
      setIsSubmitting(false)
      setIsFlipped(false)
      setCurrentIndex((prev) => prev + 1)
    }
  }

  const currentCard = cards[currentIndex]
  const isDone = !isLoading && currentIndex >= cards.length

  return (
    <div className="min-h-screen bg-bg">
      <Navbar />
      <main className="max-w-2xl mx-auto px-6 py-10">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-white text-2xl font-bold">Spaced Review</h1>
          {cards.length > 0 && !isDone && (
            <span className="text-muted text-sm">
              {currentIndex + 1} / {cards.length}
            </span>
          )}
        </div>

        {isLoading && (
          <p className="text-muted text-sm">Loading cards...</p>
        )}

        {isDone && (
          <div className="bg-surface border border-border rounded-lg p-8 text-center">
            <p className="text-gold text-2xl font-bold mb-2">All done!</p>
            <p className="text-muted text-sm">No more cards due for review right now.</p>
          </div>
        )}

        {!isLoading && !isDone && currentCard !== undefined && (
          <div className="space-y-6">
            <div onClick={!isFlipped ? handleFlip : undefined}>
              <FlashCard card={currentCard} />
            </div>

            {!isFlipped && (
              <p className="text-muted text-xs text-center">Click the card to reveal the answer</p>
            )}

            {isFlipped && (
              <div className="space-y-3">
                <p className="text-muted text-xs text-center">How well did you know this?</p>
                <QualityButtons onSelect={handleQuality} disabled={isSubmitting} />
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  )
}

export default ReviewPage
