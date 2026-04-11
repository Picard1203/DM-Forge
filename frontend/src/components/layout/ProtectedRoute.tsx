import React from 'react'
import { Navigate, Outlet } from 'react-router-dom'
import { useAuthStore } from '@/store/authStore'

const ProtectedRoute: React.FC = () => {
  const token = useAuthStore((s) => s.token)

  if (token === null) {
    return <Navigate to="/login" replace />
  }

  return <Outlet />
}

export default ProtectedRoute
