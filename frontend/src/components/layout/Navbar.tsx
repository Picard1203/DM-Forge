import React from 'react'
import { Link, NavLink, useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useAuthStore } from '@/store/authStore'

const navLinkClass = ({ isActive }: { isActive: boolean }) =>
  `text-sm transition-colors pb-0.5 border-b-2 ${
    isActive
      ? 'text-white border-amber'
      : 'text-muted hover:text-white border-transparent'
  }`

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
      <Link to="/" className="font-display text-gold font-semibold text-xl tracking-widest">
        The DM Forge
      </Link>

      <div className="flex items-center gap-6">
        <NavLink to="/curriculum" className={navLinkClass}>
          {t('nav.curriculum')}
        </NavLink>
        <NavLink to="/session" className={navLinkClass}>
          {t('nav.session')}
        </NavLink>
        <NavLink to="/review" className={navLinkClass}>
          {t('nav.review')}
        </NavLink>
        <NavLink to="/achievements" className={navLinkClass}>
          {t('nav.achievements')}
        </NavLink>
      </div>

      <div className="flex items-center gap-4">
        {user !== null && (
          <span className="text-sm text-muted">
            <span className="text-gold font-semibold">{user.username}</span>
            {' · '}
            <span className="text-white">Lv {user.level}</span>
            {' · '}
            <span className="text-gold">{user.xp.toLocaleString()} XP</span>
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
