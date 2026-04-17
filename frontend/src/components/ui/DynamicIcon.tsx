import React from 'react'
import {
  Award,
  BookOpen,
  BookText,
  Brain,
  CheckCircle,
  ClipboardList,
  Crown,
  Flag,
  Flame,
  Gem,
  Globe,
  LayoutDashboard,
  MessageCircle,
  Mic,
  Milestone,
  Rocket,
  Skull,
  Sparkles,
  Swords,
  Target,
  Trophy,
  UserPlus,
  Users,
  Wrench,
  Zap,
  type LucideIcon,
} from 'lucide-react'

const ICON_MAP: Record<string, LucideIcon> = {
  award: Award,
  'book-open': BookOpen,
  'book-text': BookText,
  brain: Brain,
  'check-circle': CheckCircle,
  'clipboard-list': ClipboardList,
  crown: Crown,
  flag: Flag,
  flame: Flame,
  gem: Gem,
  globe: Globe,
  'layout-dashboard': LayoutDashboard,
  'message-circle': MessageCircle,
  mic: Mic,
  milestone: Milestone,
  rocket: Rocket,
  skull: Skull,
  sparkles: Sparkles,
  swords: Swords,
  target: Target,
  trophy: Trophy,
  'user-plus': UserPlus,
  users: Users,
  wrench: Wrench,
  zap: Zap,
}

const SLUG_RE = /^[a-z0-9-]+$/

interface Props {
  name: string | null | undefined
  size?: number
  strokeWidth?: number
  className?: string
}

const DynamicIcon: React.FC<Props> = ({ name, size = 20, strokeWidth = 2, className }) => {
  if (name == null || name === '') {
    return <Award size={size} strokeWidth={strokeWidth} className={className} />
  }
  const Mapped = ICON_MAP[name]
  if (Mapped !== undefined) {
    return <Mapped size={size} strokeWidth={strokeWidth} className={className} />
  }
  if (!SLUG_RE.test(name)) {
    return <span className={className}>{name}</span>
  }
  return <Award size={size} strokeWidth={strokeWidth} className={className} />
}

export default DynamicIcon
