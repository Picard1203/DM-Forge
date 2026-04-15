import client from './client'
import type { AchievementResponse, UserAchievementResponse } from '@/types'

export async function listAchievements(): Promise<AchievementResponse[]> {
  const response = await client.get<AchievementResponse[]>('/achievements')
  return response.data
}

export async function getMyAchievements(): Promise<UserAchievementResponse[]> {
  const response = await client.get<UserAchievementResponse[]>('/achievements/mine')
  return response.data
}
