import client from './client'
import type { SessionPlanResponse } from '@/types'

export async function buildPlan(availableMinutes: number): Promise<SessionPlanResponse> {
  const response = await client.post<SessionPlanResponse>('/sessions/plan', {
    available_minutes: availableMinutes,
  })
  return response.data
}
