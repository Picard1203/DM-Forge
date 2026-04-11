import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useAuthStore } from '@/store/authStore'

const RegisterForm: React.FC = () => {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const register = useAuthStore((s) => s.register)
  const isLoading = useAuthStore((s) => s.isLoading)
  const error = useAuthStore((s) => s.error)
  const clearError = useAuthStore((s) => s.clearError)

  const [email, setEmail] = useState('')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    clearError()
    try {
      await register({ email, username, password })
      navigate('/')
    } catch {
      // error already set in store
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error !== null && (
        <div className="bg-primary/10 border border-primary/30 rounded px-4 py-2 text-sm text-primary">
          {t('errors.generic')}
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
        <label className="block text-sm text-muted mb-1" htmlFor="username">
          {t('auth.username')}
        </label>
        <input
          id="username"
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          minLength={3}
          maxLength={30}
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
          minLength={8}
          className="w-full bg-bg border border-border rounded px-3 py-2 text-white focus:outline-none focus:border-primary"
        />
      </div>

      <button
        type="submit"
        disabled={isLoading}
        className="w-full bg-primary hover:bg-primary/80 disabled:opacity-50 text-white font-semibold py-2 rounded transition-colors"
      >
        {isLoading ? t('common.loading') : t('auth.register')}
      </button>
    </form>
  )
}

export default RegisterForm
