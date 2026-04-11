import React from 'react'
import type { Task } from '@/types'
import TaskItem from './TaskItem'

interface Props {
  tasks: Task[]
}

const TaskList: React.FC<Props> = ({ tasks }) => {
  return (
    <ul className="space-y-2">
      {tasks.map((task) => (
        <TaskItem key={task.id} task={task} />
      ))}
    </ul>
  )
}

export default TaskList
