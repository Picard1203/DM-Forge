import client from './client'
import type { Achievement } from '@/types'

export async function listAchievements(): Promise<Achievement[]> {
  const response = await client.get<Achievement[]>('/achievements')
  return response.data
}

export async function getMyAchievements(): Promise<Achievement[]> {
  const response = await client.get<Achievement[]>('/achievements/mine')
  return response.data
}
