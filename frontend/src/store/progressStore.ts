import { create } from 'zustand'
import * as progressApi from '@/api/progress'
import type { ProgressOverviewResponse } from '@/types'

interface ProgressState {
  overview: ProgressOverviewResponse | null
  isLoading: boolean
  completedTaskIds: Set<string>
}

interface ProgressActions {
  fetchOverview: () => Promise<void>
  completeTask: (taskId: string) => Promise<void>
}

export const useProgressStore = create<ProgressState & ProgressActions>((set, get) => ({
  overview: null,
  isLoading: false,
  completedTaskIds: new Set<string>(),

  fetchOverview: async () => {
    set({ isLoading: true })
    try {
      const overview = await progressApi.getOverview()
      set({ overview, isLoading: false })
    } catch {
      set({ isLoading: false })
    }
  },

  completeTask: async (taskId: string) => {
    try {
      const result = await progressApi.completeTask(taskId)
      if (result.already_completed === false) {
        const current = get().completedTaskIds
        const updated = new Set(current)
        updated.add(taskId)
        set({ completedTaskIds: updated })
      }
      await get().fetchOverview()
    } catch {
      // silently ignore errors for now
    }
  },
}))
