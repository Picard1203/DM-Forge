import { create } from 'zustand'
import * as authApi from '@/api/auth'
import { TOKEN_KEY } from '@/api/client'
import type { User, RegisterRequest, LoginRequest } from '@/types'

interface AuthState {
  user: User | null
  token: string | null
  isLoading: boolean
  error: string | null
}

interface AuthActions {
  login: (data: LoginRequest) => Promise<void>
  register: (data: RegisterRequest) => Promise<void>
  logout: () => void
  fetchMe: () => Promise<void>
  hydrate: () => void
  clearError: () => void
}

export const useAuthStore = create<AuthState & AuthActions>((set) => ({
  user: null,
  token: localStorage.getItem(TOKEN_KEY),
  isLoading: false,
  error: null,

  hydrate: () => {
    const stored = localStorage.getItem(TOKEN_KEY)
    if (stored !== null) {
      set({ token: stored })
    }
  },

  login: async (data: LoginRequest) => {
    set({ isLoading: true, error: null })
    try {
      const tokenResponse = await authApi.login(data)
      localStorage.setItem(TOKEN_KEY, tokenResponse.access_token)
      const user = await authApi.getMe()
      set({ token: tokenResponse.access_token, user, isLoading: false })
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Login failed'
      set({ isLoading: false, error: message })
      throw err
    }
  },

  register: async (data: RegisterRequest) => {
    set({ isLoading: true, error: null })
    try {
      const tokenResponse = await authApi.register(data)
      localStorage.setItem(TOKEN_KEY, tokenResponse.access_token)
      const user = await authApi.getMe()
      set({ token: tokenResponse.access_token, user, isLoading: false })
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Registration failed'
      set({ isLoading: false, error: message })
      throw err
    }
  },

  logout: () => {
    localStorage.removeItem(TOKEN_KEY)
    set({ user: null, token: null, error: null })
  },

  fetchMe: async () => {
    set({ isLoading: true })
    try {
      const user = await authApi.getMe()
      set({ user, isLoading: false })
    } catch {
      set({ isLoading: false })
    }
  },

  clearError: () => set({ error: null }),
}))
