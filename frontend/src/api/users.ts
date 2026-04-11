import client from './client'
import type { User } from '@/types'

export async function getProfile(): Promise<User> {
  const response = await client.get<User>('/users/me')
  return response.data
}

export async function updateProfile(data: { username?: string }): Promise<User> {
  const response = await client.put<User>('/users/me', data)
  return response.data
}

export async function getStats(): Promise<unknown> {
  const response = await client.get('/users/me/stats')
  return response.data
}
