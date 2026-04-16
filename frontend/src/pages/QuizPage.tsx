import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import Navbar from '@/components/layout/Navbar'
import QuestionCard from '@/components/quiz/QuestionCard'
import QuizResult from '@/components/quiz/QuizResult'
import * as quizzesApi from '@/api/quizzes'
import type { Quiz, QuizResult as QuizResultType } from '@/types'
import { useToastStore } from '@/store/toastStore'

const QuizPage: React.FC = () => {
  const { quizId } = useParams<{ quizId: string }>()
  const [quiz, setQuiz] = useState<Quiz | null>(null)
  const [isLoading, setIsLoading] = useState<boolean>(true)
  const [currentIndex, setCurrentIndex] = useState<number>(0)
  const [answers, setAnswers] = useState<number[]>([])
  const [result, setResult] = useState<QuizResultType | null>(null)
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false)
  const pushToast = useToastStore((s) => s.push)

  useEffect(() => {
    if (quizId === undefined) return
    quizzesApi.getQuiz(quizId).then((data) => {
      setQuiz(data)
      setAnswers(new Array(data.questions.length).fill(-1))
      setIsLoading(false)
    }).catch(() => {
      setIsLoading(false)
    })
  }, [quizId])

  const handleSelect = (index: number) => {
    setAnswers((prev) => {
      const updated = [...prev]
      updated[currentIndex] = index
      return updated
    })
  }

  const handleNext = () => {
    if (quiz !== null && currentIndex < quiz.questions.length - 1) {
      setCurrentIndex((prev) => prev + 1)
    }
  }

  const handleSubmit = async () => {
    if (quiz === null || quizId === undefined) return
    setIsSubmitting(true)
    try {
      const quizResult = await quizzesApi.submitQuiz(quizId, answers)
      setResult(quizResult)
      for (const achievement of quizResult.earned_achievements) {
        pushToast({ title: 'Achievement Unlocked!', message: achievement.title })
      }
    } catch {
      // ignore
    } finally {
      setIsSubmitting(false)
    }
  }

  const isLastQuestion = quiz !== null && currentIndex === quiz.questions.length - 1
  const currentAnswer = answers[currentIndex] ?? -1

  return (
    <div className="min-h-screen bg-bg">
      <Navbar />
      <main className="max-w-2xl mx-auto px-6 py-10">
        {isLoading && (
          <p className="text-muted text-sm">Loading quiz...</p>
        )}

        {!isLoading && quiz === null && (
          <p className="text-muted text-sm">Quiz not found.</p>
        )}

        {quiz !== null && result !== null && (
          <div>
            <h1 className="text-white text-2xl font-bold mb-6">{quiz.title}</h1>
            <QuizResult result={result} />
          </div>
        )}

        {quiz !== null && result === null && (
          <div>
            <div className="flex items-center justify-between mb-6">
              <h1 className="text-white text-2xl font-bold">{quiz.title}</h1>
              <span className="text-muted text-sm">
                {currentIndex + 1} / {quiz.questions.length}
              </span>
            </div>

            <QuestionCard
              question={quiz.questions[currentIndex]}
              selectedIndex={currentAnswer === -1 ? null : currentAnswer}
              onSelect={handleSelect}
            />

            <div className="mt-6 flex justify-end">
              {!isLastQuestion && (
                <button
                  onClick={handleNext}
                  disabled={currentAnswer === -1}
                  className="px-6 py-2 bg-primary text-bg rounded-lg text-sm font-medium disabled:opacity-40 hover:bg-primary/90 transition-colors"
                >
                  Next
                </button>
              )}
              {isLastQuestion && (
                <button
                  onClick={handleSubmit}
                  disabled={currentAnswer === -1 || isSubmitting}
                  className="px-6 py-2 bg-gold text-bg rounded-lg text-sm font-medium disabled:opacity-40 hover:bg-gold/90 transition-colors"
                >
                  {isSubmitting ? 'Submitting...' : 'Submit Quiz'}
                </button>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default QuizPage
