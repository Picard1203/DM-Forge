import { create } from 'zustand'
import type { ProgressOverview } from '@/types'

interface ProgressState {
  overview: ProgressOverview | null
  isLoading: boolean
}

interface ProgressActions {
  setOverview: (overview: ProgressOverview) => void
}

export const useProgressStore = create<ProgressState & ProgressActions>((set) => ({
  overview: null,
  isLoading: false,
  setOverview: (overview: ProgressOverview) => set({ overview }),
}))
