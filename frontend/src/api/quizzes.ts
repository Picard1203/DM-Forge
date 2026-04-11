import client from './client'
import type { Quiz, QuizResult } from '@/types'

export async function getQuiz(quizId: string): Promise<Quiz> {
  const response = await client.get<Quiz>(`/quizzes/${quizId}`)
  return response.data
}

export async function submitQuiz(
  quizId: string,
  answers: Array<{ question_id: string; selected_index: number }>
): Promise<QuizResult> {
  const response = await client.post<QuizResult>(`/quizzes/${quizId}/submit`, { answers })
  return response.data
}
