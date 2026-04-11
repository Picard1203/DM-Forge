import client from './client'
import type { Module, Task } from '@/types'

export async function getModules(): Promise<Module[]> {
  const response = await client.get<Module[]>('/modules')
  return response.data
}

export async function getModule(slug: string): Promise<Module> {
  const response = await client.get<Module>(`/modules/${slug}`)
  return response.data
}

export async function getModuleTasks(slug: string): Promise<Task[]> {
  const response = await client.get<Task[]>(`/modules/${slug}/tasks`)
  return response.data
}
