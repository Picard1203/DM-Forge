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

export type TaskType =
  | 'reading'
  | 'video'
  | 'podcast'
  | 'exercise'
  | 'tool_exploration'
  | 'quiz_ref'

export interface Module {
  id: string
  slug: string
  title: string
  description: string
  order: number
  icon: string | null
  is_extension: boolean
  estimated_hours: number
  xp_reward: number
}

export interface Task {
  id: string
  slug: string
  title: string
  description: string
  order: number
  task_type: TaskType
  estimated_minutes: number
  xp_reward: number
  content: Record<string, unknown>
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
  scenario_context?: string
  order: number
}

export interface QuizQuestionResult {
  question_index: number
  correct: boolean
  correct_answer_index: number
  explanation: string
}

export interface AchievementResponse {
  id: string
  slug: string
  title: string
  description: string
  icon: string
  xp_reward: number
}

export interface UserAchievementResponse {
  id: string
  slug: string
  title: string
  description: string
  icon: string
  xp_reward: number
  earned_at: string
}

export interface CompleteTaskResponse {
  already_completed: boolean
  xp_earned: number
  new_xp: number
  new_level: number
  earned_achievements: AchievementResponse[]
}

export interface ModuleProgressItem {
  module_id: string
  completed: number
  total: number
  percent: number
}

export interface ProgressOverviewResponse {
  modules: ModuleProgressItem[]
  total_xp: number
}

export interface QuizResult {
  score: number
  passed: boolean
  xp_earned: number
  already_completed: boolean
  question_results: QuizQuestionResult[]
  earned_achievements: AchievementResponse[]
}

export interface ReviewCard {
  id: string
  front: string
  back: string
  tags: string[]
}

export interface ReviewSubmitResponse {
  next_review: string
  interval_days: number
  ease_factor: number
}

export interface SessionTaskItem {
  task_id: string
  slug: string
  title: string
  task_type: string
  estimated_minutes: number
  xp_reward: number
}

export interface SessionPlanResponse {
  tasks: SessionTaskItem[]
  total_minutes: number
  has_review_slot: boolean
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
