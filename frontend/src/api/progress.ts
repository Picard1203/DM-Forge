import client from './client'
import type { CompleteTaskResponse, ProgressOverviewResponse } from '@/types'

export async function getOverview(): Promise<ProgressOverviewResponse> {
  const response = await client.get<ProgressOverviewResponse>('/progress/overview')
  return response.data
}

export async function completeTask(taskId: string): Promise<CompleteTaskResponse> {
  const response = await client.post<CompleteTaskResponse>('/progress/complete', { task_id: taskId })
  return response.data
}
