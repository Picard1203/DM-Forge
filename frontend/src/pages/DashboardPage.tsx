import React, { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import { CheckCircle } from 'lucide-react'
import { useAuthStore } from '@/store/authStore'
import { useProgressStore } from '@/store/progressStore'
import Navbar from '@/components/layout/Navbar'
import StreakWidget from '@/components/dashboard/StreakWidget'
import XPBar from '@/components/progress/XPBar'
import * as curriculumApi from '@/api/curriculum'
import { progressBarClass } from '@/utils/progressColor'
import type { Module, ModuleProgressItem } from '@/types'

const DashboardPage: React.FC = () => {
  const { t } = useTranslation()
  const user = useAuthStore((s) => s.user)
  const fetchMe = useAuthStore((s) => s.fetchMe)
  const overview = useProgressStore((s) => s.overview)
  const fetchOverview = useProgressStore((s) => s.fetchOverview)
  const [modules, setModules] = useState<Module[]>([])

  useEffect(() => {
    fetchMe()
    fetchOverview()
    curriculumApi.getModules().then(setModules).catch(() => {})
  }, [fetchMe, fetchOverview])

  const getModuleProgress = (moduleId: string): ModuleProgressItem | null => {
    if (overview === null) {
      return null
    }
    for (const item of overview.modules) {
      if (item.module_id === moduleId) {
        return item
      }
    }
    return null
  }

  return (
    <div className="min-h-screen bg-bg">
      <Navbar />
      <main className="max-w-5xl mx-auto px-6 py-10">
        {user !== null && (
          <>
            <div className="mb-6">
              <h1 className="font-display text-3xl md:text-4xl font-bold tracking-wide text-white">
                {t('dashboard.welcome', { username: user.username })}
              </h1>
            </div>

            <div className="mb-8">
              <XPBar xp={user.xp} level={user.level} title={user.avatar_title} />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
              <StreakWidget
                currentStreak={user.current_streak}
                longestStreak={user.longest_streak}
              />
            </div>

            {modules.length > 0 && (
              <div>
                <h2 className="font-display text-xl md:text-2xl font-semibold tracking-wide text-white mb-4">
                  {t('progress.modules_heading', 'Module Progress')}
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {modules.map((module) => {
                    const progress = getModuleProgress(module.id)
                    const percent = progress !== null ? progress.percent : 0
                    const completed = progress !== null ? progress.completed : 0
                    const total = progress !== null ? progress.total : 0
                    const isComplete = percent >= 100
                    return (
                      <div
                        key={module.id}
                        className={`card-surface p-4 relative ${isComplete ? 'card-complete' : ''}`}
                      >
                        {isComplete && (
                          <div className="absolute top-3 right-3">
                            <CheckCircle size={16} className="text-gold" />
                          </div>
                        )}
                        <p className="text-white text-sm font-semibold mb-2 pr-6">{module.title}</p>
                        <div className="w-full bg-bg rounded-full h-1.5 mb-1 overflow-hidden">
                          <div
                            className={`h-1.5 rounded-full transition-all duration-500 ${progressBarClass(percent)}`}
                            style={{ width: `${percent}%` }}
                          />
                        </div>
                        <p className="text-muted text-xs">
                          {completed}/{total} {t('progress.tasks_done', { count: completed })}
                        </p>
                      </div>
                    )
                  })}
                </div>
              </div>
            )}
          </>
        )}
      </main>
    </div>
  )
}

export default DashboardPage
