import React, { useEffect, useState } from 'react'
import { useTranslation } from 'react-i18next'
import Navbar from '@/components/layout/Navbar'
import * as sessionsApi from '@/api/sessions'
import type { SessionPlanResponse, SessionTaskItem } from '@/types'

const SLIDER_MIN = 15
const SLIDER_MAX = 120
const SLIDER_STEP = 15

const SessionPage: React.FC = () => {
  const { t } = useTranslation()
  const [availableMinutes, setAvailableMinutes] = useState<number>(30)
  const [plan, setPlan] = useState<SessionPlanResponse | null>(null)
  const [isLoading, setIsLoading] = useState<boolean>(false)

  useEffect(() => {
    handleSliderChange(availableMinutes)
  }, [])

  const handleSliderChange = async (value: number) => {
    setAvailableMinutes(value)
    setIsLoading(true)
    try {
      const result = await sessionsApi.buildPlan(value)
      setPlan(result)
    } catch {
      setPlan(null)
    } finally {
      setIsLoading(false)
    }
  }

  const renderTaskCard = (item: SessionTaskItem) => (
    <div key={item.task_id} className="bg-surface border border-border rounded-lg p-4">
      <div className="flex items-start justify-between gap-4 mb-1">
        <p className="text-white text-sm font-medium">{item.title}</p>
        <span className="text-muted text-xs uppercase tracking-wider shrink-0">{item.task_type}</span>
      </div>
      <div className="flex gap-3">
        <span className="text-muted text-xs">{item.estimated_minutes} min</span>
        <span className="text-gold text-xs">{item.xp_reward} XP</span>
      </div>
    </div>
  )

  return (
    <div className="min-h-screen bg-bg">
      <Navbar />
      <main className="max-w-2xl mx-auto px-6 py-10">
        <h1 className="text-white text-2xl font-bold mb-6">Plan a Session</h1>

        <div className="bg-surface border border-border rounded-lg p-6 mb-6">
          <label className="block text-white text-sm font-medium mb-3">
            Available time: <span className="text-gold">{availableMinutes} minutes</span>
          </label>
          <input
            type="range"
            min={SLIDER_MIN}
            max={SLIDER_MAX}
            step={SLIDER_STEP}
            value={availableMinutes}
            onChange={(e) => handleSliderChange(Number(e.target.value))}
            className="w-full accent-gold"
          />
          <div className="flex justify-between text-muted text-xs mt-1">
            <span>{SLIDER_MIN} min</span>
            <span>{SLIDER_MAX} min</span>
          </div>
        </div>

        {isLoading && (
          <p className="text-muted text-sm">{t('common.loading')}</p>
        )}

        {plan !== null && (
          <div>
            <div className="flex items-center gap-4 mb-4">
              <p className="text-muted text-sm">
                Total: <span className="text-white">{plan.total_minutes} min</span>
              </p>
              {plan.has_review_slot && (
                <span className="text-xs bg-gold/10 text-gold border border-gold/30 rounded px-2 py-0.5">
                  + 5 min review slot
                </span>
              )}
            </div>

            {plan.tasks.length === 0 ? (
              <p className="text-muted text-sm">No incomplete tasks fit this time window.</p>
            ) : (
              <div className="space-y-3">
                {plan.tasks.map(renderTaskCard)}
              </div>
            )}

            <p className="mt-6 text-muted text-sm text-center">
              Tasks are completed from the module pages.
            </p>
          </div>
        )}
      </main>
    </div>
  )
}

export default SessionPage
