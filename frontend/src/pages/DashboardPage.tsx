import React, { useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { useAuthStore } from '@/store/authStore'
import Navbar from '@/components/layout/Navbar'
import StatsCard from '@/components/dashboard/StatsCard'
import StreakWidget from '@/components/dashboard/StreakWidget'
import NextUpCard from '@/components/dashboard/NextUpCard'

const DashboardPage: React.FC = () => {
  const { t } = useTranslation()
  const user = useAuthStore((s) => s.user)
  const fetchMe = useAuthStore((s) => s.fetchMe)

  useEffect(() => {
    if (user === null) {
      fetchMe()
    }
  }, [user, fetchMe])

  return (
    <div className="min-h-screen bg-bg">
      <Navbar />
      <main className="max-w-5xl mx-auto px-6 py-10">
        {user !== null && (
          <>
            <div className="mb-8">
              <h1 className="text-white text-3xl font-bold">
                {t('dashboard.welcome', { username: user.username })}
              </h1>
              <p className="text-gold mt-1">
                {user.avatar_title} · {t('dashboard.level', { level: user.level })}
              </p>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
              <StatsCard label="XP" value={user.xp.toLocaleString()} />
              <StatsCard label="Level" value={user.level} />
              <StreakWidget
                currentStreak={user.current_streak}
                longestStreak={user.longest_streak}
              />
              <NextUpCard />
            </div>
          </>
        )}
      </main>
    </div>
  )
}

export default DashboardPage
