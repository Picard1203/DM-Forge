import { create } from 'zustand'

export interface Toast {
  id: string
  title: string
  message: string
}

interface ToastState {
  toasts: Toast[]
}

interface ToastActions {
  push: (toast: Omit<Toast, 'id'>) => void
  dismiss: (id: string) => void
}

export const useToastStore = create<ToastState & ToastActions>((set) => ({
  toasts: [],

  push: (toast) => {
    const id = `${Date.now()}-${Math.random()}`
    set((state) => ({ toasts: [...state.toasts, { ...toast, id }] }))
    setTimeout(() => {
      set((state) => ({ toasts: state.toasts.filter((t) => t.id !== id) }))
    }, 4000)
  },

  dismiss: (id) => {
    set((state) => ({ toasts: state.toasts.filter((t) => t.id !== id) }))
  },
}))
