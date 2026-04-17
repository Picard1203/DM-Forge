export function progressBarClass(percent: number): string {
  if (percent >= 100) return 'bg-emerald-500'
  if (percent >= 75) return 'bg-gold'
  if (percent >= 25) return 'bg-amber'
  return 'bg-amber/60'
}
