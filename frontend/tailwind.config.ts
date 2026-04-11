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
        surface: '#12182b',
        border: '#1e2a3a',
        muted: '#6b7a99',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}

export default config
