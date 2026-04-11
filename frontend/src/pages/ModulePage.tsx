import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import Navbar from '@/components/layout/Navbar'
import TaskCard from '@/components/curriculum/TaskCard'
import { getModule, getModuleTasks } from '@/api/curriculum'
import type { Module, Task } from '@/types'

const ModulePage: React.FC = () => {
  const { slug } = useParams<{ slug: string }>()
  const [module, setModule] = useState<Module | null>(null)
  const [tasks, setTasks] = useState<Task[] | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (slug === undefined) {
      return
    }
    const load = async () => {
      try {
        const [moduleData, tasksData] = await Promise.all([
          getModule(slug),
          getModuleTasks(slug),
        ])
        setModule(moduleData)
        setTasks(tasksData)
      } catch {
        setError('Module not found.')
      }
    }
    load()
  }, [slug])

  const renderHeader = (mod: Module) => (
    <div className="mb-8">
      {mod.icon !== null && (
        <p className="text-gold text-3xl mb-2">{mod.icon}</p>
      )}
      <h1 className="text-white text-2xl font-bold">{mod.title}</h1>
      <p className="text-muted mt-2">{mod.description}</p>
      <div className="flex gap-4 mt-3">
        <span className="text-muted text-xs uppercase tracking-wider">
          {mod.estimated_hours}h estimated
        </span>
        <span className="text-gold text-xs uppercase tracking-wider">
          {mod.xp_reward} XP
        </span>
      </div>
    </div>
  )

  const renderTasks = (taskList: Task[]) => {
    const cards: React.ReactElement[] = []
    for (const task of taskList) {
      cards.push(<TaskCard key={task.id} task={task} />)
    }
    return <div className="space-y-3">{cards}</div>
  }

  const renderContent = () => {
    if (error !== null) {
      return <p className="text-primary">{error}</p>
    }
    if (module === null || tasks === null) {
      return <p className="text-muted">Loading...</p>
    }
    return (
      <>
        {renderHeader(module)}
        {renderTasks(tasks)}
      </>
    )
  }

  return (
    <div className="min-h-screen bg-bg">
      <Navbar />
      <main className="max-w-5xl mx-auto px-6 py-10">
        {renderContent()}
      </main>
    </div>
  )
}

export default ModulePage
