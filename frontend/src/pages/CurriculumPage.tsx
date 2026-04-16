import React, { useEffect, useState } from 'react'
import Navbar from '@/components/layout/Navbar'
import ModuleCard from '@/components/curriculum/ModuleCard'
import { getModules } from '@/api/curriculum'
import { useProgressStore } from '@/store/progressStore'
import type { Module } from '@/types'

const CurriculumPage: React.FC = () => {
  const [modules, setModules] = useState<Module[] | null>(null)
  const [error, setError] = useState<string | null>(null)
  const fetchOverview = useProgressStore((s) => s.fetchOverview)
  const overview = useProgressStore((s) => s.overview)

  useEffect(() => {
    const load = async () => {
      try {
        const data = await getModules()
        setModules(data)
      } catch {
        setError('Failed to load curriculum.')
      }
    }
    load()
    fetchOverview()
  }, [fetchOverview])

  const getProgressPercent = (moduleId: string): number => {
    if (overview === null) return 0
    for (const item of overview.modules) {
      if (item.module_id === moduleId) return item.percent
    }
    return 0
  }

  const renderContent = () => {
    if (error !== null) {
      return <p className="text-primary">{error}</p>
    }
    if (modules === null) {
      return <p className="text-muted">Loading...</p>
    }
    const cards: React.ReactElement[] = []
    for (const mod of modules) {
      cards.push(
        <ModuleCard
          key={mod.id}
          module={mod}
          progressPercent={getProgressPercent(mod.id)}
        />
      )
    }
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {cards}
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-bg">
      <Navbar />
      <main className="max-w-5xl mx-auto px-6 py-10">
        <h1 className="text-white text-2xl font-bold mb-6">Curriculum</h1>
        {renderContent()}
      </main>
    </div>
  )
}

export default CurriculumPage
