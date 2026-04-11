import client from './client'
import type { Module, ModuleDetail } from '@/types'

export async function listModules(): Promise<Module[]> {
  const response = await client.get<Module[]>('/modules')
  return response.data
}

export async function getModule(moduleId: string): Promise<ModuleDetail> {
  const response = await client.get<ModuleDetail>(`/modules/${moduleId}`)
  return response.data
}
