import client from './client'
import type { SessionPlan } from '@/types'

export async function buildPlan(availableMinutes: number): Promise<SessionPlan> {
  const response = await client.post<SessionPlan>('/sessions/plan', {
    available_minutes: availableMinutes,
  })
  return response.data
}
