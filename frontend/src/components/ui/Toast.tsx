import React from 'react'
import { useToastStore } from '@/store/toastStore'

const ToastContainer: React.FC = () => {
  const toasts = useToastStore((s) => s.toasts)
  const dismiss = useToastStore((s) => s.dismiss)

  if (toasts.length === 0) return null

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col gap-3 max-w-xs">
      {toasts.map((toast) => (
        <div
          key={toast.id}
          className="bg-surface border border-gold/40 rounded-lg px-4 py-3 shadow-lg flex items-start gap-3 animate-fade-in"
        >
          <span className="text-gold text-lg">★</span>
          <div className="flex-1 min-w-0">
            <p className="text-gold text-xs font-semibold uppercase tracking-wider">
              {toast.title}
            </p>
            <p className="text-white text-sm">{toast.message}</p>
          </div>
          <button
            onClick={() => dismiss(toast.id)}
            className="text-muted hover:text-white text-lg leading-none shrink-0"
            aria-label="Dismiss"
          >
            ×
          </button>
        </div>
      ))}
    </div>
  )
}

export default ToastContainer
