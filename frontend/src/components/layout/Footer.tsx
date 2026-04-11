import React from 'react'

const Footer: React.FC = () => {
  return (
    <footer className="bg-surface border-t border-border px-6 py-3 text-center text-muted text-xs">
      The DM Forge © {new Date().getFullYear()}
    </footer>
  )
}

export default Footer
