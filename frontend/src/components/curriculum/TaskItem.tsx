import React from 'react'
import type { Task } from '@/types'

interface Props {
  task: Task
}

const TaskItem: React.FC<Props> = ({ task }) => {
  return (
    <li className="bg-surface border border-border rounded px-4 py-3 flex items-center justify-between">
      <div>
        <p className="text-white text-sm font-medium">{task.title}</p>
        <p className="text-muted text-xs mt-0.5">{task.estimated_minutes} min · {task.xp_reward} XP</p>
      </div>
      <span className="text-xs text-muted uppercase">{task.task_type}</span>
    </li>
  )
}

export default TaskItem
