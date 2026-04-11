import React from 'react'
import { Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import RegisterForm from '@/components/auth/RegisterForm'

const RegisterPage: React.FC = () => {
  const { t } = useTranslation()

  return (
    <div className="min-h-screen bg-bg flex items-center justify-center px-4">
      <div className="w-full max-w-sm">
        <h1 className="text-gold text-3xl font-bold text-center mb-2">The DM Forge</h1>
        <p className="text-muted text-center text-sm mb-8">Your journey begins here</p>

        <div className="bg-surface border border-border rounded-xl p-6 space-y-6">
          <h2 className="text-white text-xl font-semibold">{t('auth.register')}</h2>
          <RegisterForm />
          <p className="text-muted text-sm text-center">
            {t('auth.have_account')}{' '}
            <Link to="/login" className="text-primary hover:underline">
              {t('auth.sign_in')}
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}

export default RegisterPage
