import React, { useEffect } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from '@/store/authStore'
import ProtectedRoute from '@/components/layout/ProtectedRoute'
import LoginPage from '@/pages/LoginPage'
import RegisterPage from '@/pages/RegisterPage'
import DashboardPage from '@/pages/DashboardPage'
import CurriculumPage from '@/pages/CurriculumPage'
import ModulePage from '@/pages/ModulePage'
import QuizPage from '@/pages/QuizPage'
import ReviewPage from '@/pages/ReviewPage'
import SessionPage from '@/pages/SessionPage'
import AchievementsPage from '@/pages/AchievementsPage'
import SettingsPage from '@/pages/SettingsPage'
import ToastContainer from '@/components/ui/Toast'

const App: React.FC = () => {
  const hydrate = useAuthStore((s) => s.hydrate)
  const fetchMe = useAuthStore((s) => s.fetchMe)
  const token = useAuthStore((s) => s.token)

  useEffect(() => {
    hydrate()
  }, [hydrate])

  useEffect(() => {
    if (token !== null) {
      fetchMe()
    }
  }, [token, fetchMe])

  return (
    <>
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      <Route element={<ProtectedRoute />}>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/curriculum" element={<CurriculumPage />} />
        <Route path="/curriculum/:slug" element={<ModulePage />} />
        <Route path="/quiz/:quizId" element={<QuizPage />} />
        <Route path="/review" element={<ReviewPage />} />
        <Route path="/session" element={<SessionPage />} />
        <Route path="/achievements" element={<AchievementsPage />} />
        <Route path="/settings" element={<SettingsPage />} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
    <ToastContainer />
    </>
  )
}

export default App
