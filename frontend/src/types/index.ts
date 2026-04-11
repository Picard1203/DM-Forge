export interface User {
  id: string
  email: string
  username: string
  avatar_title: string
  xp: number
  level: number
  current_streak: number
  longest_streak: number
}

export interface Module {
  id: string
  slug: string
  title: string
  description: string
  order: number
  estimated_minutes: number
  icon: string
  is_extension: boolean
}

export interface Task {
  id: string
  module_id: string
  slug: string
  title: string
  task_type: string
  content_url: string | null
  description: string
  order: number
  estimated_minutes: number
  xp_reward: number
  tags: string[]
}

export interface ModuleDetail extends Module {
  tasks: Task[]
}

export interface Quiz {
  id: string
  module_id: string
  title: string
  description: string
  passing_score: number
  xp_reward: number
  questions: QuizQuestion[]
}

export interface QuizQuestion {
  id: string
  question_text: string
  question_type: string
  options: string[]
  order: number
}

export interface QuizResult {
  score: number
  passed: boolean
  xp_awarded: number
  correct_count: number
  total_count: number
}

export interface ModuleProgress {
  module_id: string
  tasks_completed: number
  tasks_total: number
  percent_complete: number
}

export interface ProgressOverview {
  modules: ModuleProgress[]
  total_tasks_completed: number
  total_xp: number
}

export interface Achievement {
  id: string
  slug: string
  title: string
  description: string
  icon: string
  xp_reward: number
  earned_at?: string
}

export interface ReviewCard {
  review_id: string
  card_id: string
  front: string
  back: string
  module_id: string
}

export interface ReviewSubmitResponse {
  review_id: string
  next_review_at: string
  interval_days: number
}

export interface SessionTaskItem {
  task: Task
  estimated_minutes: number
}

export interface SessionPlan {
  items: SessionTaskItem[]
  total_minutes: number
  xp_potential: number
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

export interface RegisterRequest {
  email: string
  username: string
  password: string
}

export interface LoginRequest {
  email: string
  password: string
}
