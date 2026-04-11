import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useAuthStore } from '@/store/authStore'

const LoginForm: React.FC = () => {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const login = useAuthStore((s) => s.login)
  const isLoading = useAuthStore((s) => s.isLoading)
  const error = useAuthStore((s) => s.error)
  const clearError = useAuthStore((s) => s.clearError)

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    clearError()
    try {
      await login({ email, password })
      navigate('/')
    } catch {
      // error already set in store
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error !== null && (
        <div className="bg-primary/10 border border-primary/30 rounded px-4 py-2 text-sm text-primary">
          {t('errors.invalid_credentials')}
        </div>
      )}

      <div>
        <label className="block text-sm text-muted mb-1" htmlFor="email">
          {t('auth.email')}
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="w-full bg-bg border border-border rounded px-3 py-2 text-white focus:outline-none focus:border-primary"
        />
      </div>

      <div>
        <label className="block text-sm text-muted mb-1" htmlFor="password">
          {t('auth.password')}
        </label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="w-full bg-bg border border-border rounded px-3 py-2 text-white focus:outline-none focus:border-primary"
        />
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="w-full bg-primary hover:bg-primary/80 disabled:opacity-50 text-white font-semibold py-2 rounded transition-colors"
      >
        {isLoading ? t('common.loading') : t('auth.login')}
      </button>
    </form>
  )
}

export default LoginForm
