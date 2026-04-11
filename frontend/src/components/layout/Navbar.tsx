import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useAuthStore } from '@/store/authStore'

const Navbar: React.FC = () => {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const user = useAuthStore((s) => s.user)
  const logout = useAuthStore((s) => s.logout)

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav className="bg-surface border-b border-border px-6 py-3 flex items-center justify-between">
      <Link to="/" className="text-gold font-bold text-lg tracking-wide">
        The DM Forge
      </Link>

      <div className="flex items-center gap-6">
        <Link to="/curriculum" className="text-muted hover:text-white text-sm transition-colors">
          {t('nav.curriculum')}
        </Link>
        <Link to="/session" className="text-muted hover:text-white text-sm transition-colors">
          {t('nav.session')}
        </Link>
        <Link to="/review" className="text-muted hover:text-white text-sm transition-colors">
          {t('nav.review')}
        </Link>
        <Link to="/achievements" className="text-muted hover:text-white text-sm transition-colors">
          {t('nav.achievements')}
        </Link>
      </div>

      <div className="flex items-center gap-4">
        {user !== null && (
          <span className="text-sm text-muted">
            <span className="text-gold font-semibold">{user.username}</span>
            {' · '}
            <span className="text-white">Lv {user.level}</span>
            {' · '}
            <span className="text-gold">{user.xp} XP</span>
          </span>
        )}
        <button
          onClick={handleLogout}
          className="text-sm text-muted hover:text-primary transition-colors"
        >
          {t('auth.logout')}
        </button>
      </div>
    </nav>
  )
}

export default Navbar
