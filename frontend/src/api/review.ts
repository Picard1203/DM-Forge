import client from './client'
import type { ReviewCard, ReviewSubmitResponse } from '@/types'

export async function getDueCards(): Promise<ReviewCard[]> {
  const response = await client.get<ReviewCard[]>('/review/due')
  return response.data
}

export async function submitReview(
  cardId: string,
  quality: number
): Promise<ReviewSubmitResponse> {
  const response = await client.post<ReviewSubmitResponse>('/review/submit', {
    card_id: cardId,
    quality,
  })
  return response.data
}
