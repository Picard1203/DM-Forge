import React from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import LoginForm from '@/components/auth/LoginForm'

const LoginPage: React.FC = () => {
  const { t } = useTranslation()

  return (
    <div className="min-h-screen bg-bg flex items-center justify-center px-4">
      <div className="w-full max-w-sm">
        <h1 className="text-gold text-3xl font-bold text-center mb-2">The DM Forge</h1>
        <p className="text-muted text-center text-sm mb-8">Master the art of the Dungeon Master</p>

        <div className="bg-surface border border-border rounded-xl p-6 space-y-6">
          <h2 className="text-white text-xl font-semibold">{t('auth.login')}</h2>
          <LoginForm />
          <p className="text-muted text-sm text-center">
            {t('auth.no_account')}{' '}
            <Link to="/register" className="text-primary hover:underline">
              {t('auth.sign_up')}
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}

export default LoginPage
