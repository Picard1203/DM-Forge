import React from 'react'
import type { Task } from '@/types'

interface Props {
  task: Task
}

const TaskCard: React.FC<Props> = ({ task }) => {
  const renderBody = () => {
    if (task.task_type === 'video') {
      const content = task.content as { youtube_url?: string }
      return (
        <a
          href={content.youtube_url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-primary text-sm hover:underline"
        >
          Watch on YouTube
        </a>
      )
    }
    if (task.task_type === 'reading') {
      const content = task.content as { page_start?: number; page_end?: number }
      return (
        <p className="text-muted text-sm">
          Pages {content.page_start}–{content.page_end}
        </p>
      )
    }
    if (task.task_type === 'podcast') {
      const content = task.content as { podcast_url?: string }
      return (
        <a
          href={content.podcast_url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-primary text-sm hover:underline"
        >
          Listen
        </a>
      )
    }
    if (task.task_type === 'exercise') {
      const content = task.content as { instructions?: string }
      return <p className="text-muted text-sm">{content.instructions}</p>
    }
    if (task.task_type === 'tool_exploration') {
      const content = task.content as { tool_url?: string }
      return (
        <a
          href={content.tool_url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-primary text-sm hover:underline"
        >
          Open Tool
        </a>
      )
    }
    if (task.task_type === 'quiz_ref') {
      return (
        <button
          disabled
          title="Coming soon"
          className="text-muted text-sm border border-border rounded px-3 py-1 cursor-not-allowed opacity-50"
        >
          Take Quiz
        </button>
      )
    }
    return null
  }

  return (
    <div className="bg-surface border border-border rounded-lg p-4">
      <div className="flex items-start justify-between gap-4 mb-2">
        <p className="text-white text-sm font-medium">{task.title}</p>
        <span className="text-muted text-xs uppercase tracking-wider shrink-0">
          {task.task_type}
        </span>
      </div>
      <div className="flex gap-3 mb-3">
        <span className="text-muted text-xs">{task.estimated_minutes} min</span>
        <span className="text-gold text-xs">{task.xp_reward} XP</span>
      </div>
      {renderBody()}
    </div>
  )
}

export default TaskCard
