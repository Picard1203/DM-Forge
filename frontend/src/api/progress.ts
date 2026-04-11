import client from './client'
import type { ProgressOverview } from '@/types'

export async function getOverview(): Promise<ProgressOverview> {
  const response = await client.get<ProgressOverview>('/progress/overview')
  return response.data
}

export async function completeTask(taskId: string, moduleId: string): Promise<unknown> {
  const response = await client.post('/progress/complete', { task_id: taskId, module_id: moduleId })
  return response.data
}
