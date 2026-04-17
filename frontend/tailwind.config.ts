import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './index.html',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        bg: '#0a0e1a',
        primary: '#CC3333',
        gold: '#C9A84C',
        amber: '#E8B14F',
        surface: '#12182b',
        border: '#1e2a3a',
        muted: '#6b7a99',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Cinzel', 'ui-serif', 'Georgia', 'serif'],
      },
      backgroundImage: {
        'card-surface': 'linear-gradient(180deg, #161d35 0%, #0f1527 100%)',
        'card-surface-hover': 'linear-gradient(180deg, #1a2240 0%, #121831 100%)',
      },
      boxShadow: {
        card: '0 1px 0 0 rgba(255,255,255,0.04) inset, 0 8px 24px -12px rgba(0,0,0,0.6)',
        'card-hover': '0 1px 0 0 rgba(255,255,255,0.06) inset, 0 16px 40px -16px rgba(0,0,0,0.75)',
        'card-complete': '0 0 0 1px rgba(201,168,76,0.4), 0 12px 32px -16px rgba(201,168,76,0.25)',
      },
      keyframes: {
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' },
        },
      },
      animation: {
        shimmer: 'shimmer 1.6s ease-out 1 forwards',
      },
    },
  },
  plugins: [],
}

export default config
