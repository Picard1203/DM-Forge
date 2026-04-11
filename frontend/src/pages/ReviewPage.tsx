import React from 'react'
import Navbar from '@/components/layout/Navbar'

const ReviewPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-bg">
      <Navbar />
      <main className="max-w-2xl mx-auto px-6 py-10">
        <h1 className="text-white text-2xl font-bold mb-6">Spaced Review</h1>
        <p className="text-muted">Flashcard review — coming soon</p>
      </main>
    </div>
  )
}

export default ReviewPage
