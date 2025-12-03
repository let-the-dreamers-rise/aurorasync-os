import { motion, AnimatePresence } from 'framer-motion'
import { NavLink } from 'react-router-dom'
import { 
  LayoutDashboard, 
  Car, 
  Brain, 
  Calendar, 
  Mic, 
  Wrench, 
  TrendingUp, 
  Shield,
  X
} from 'lucide-react'
import { cn } from '@/utils/cn'
import { useStore } from '@/store/useStore'

const Sidebar = () => {
  const { sidebarOpen, toggleSidebar } = useStore()

  const navItems = [
    { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
    { path: '/vehicles', icon: Car, label: 'Vehicles' },
    { path: '/predictions', icon: Brain, label: 'Predictions' },
    { path: '/scheduling', icon: Calendar, label: 'Scheduling' },
    { path: '/voice', icon: Mic, label: 'AI Conversations' },
    { path: '/workshops', icon: Wrench, label: 'Workshops' },
    { path: '/insights', icon: TrendingUp, label: 'RCA Insights' },
    { path: '/system', icon: Shield, label: 'System Health' },
  ]

  return (
    <>
      {/* Overlay for mobile */}
      <AnimatePresence>
        {sidebarOpen && (
          <motion.div
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 lg:hidden"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={toggleSidebar}
          />
        )}
      </AnimatePresence>

      {/* Sidebar */}
      <AnimatePresence>
        {sidebarOpen && (
          <motion.aside
            className="fixed left-0 top-0 h-screen w-64 glass border-r border-aurora-bg-tertiary z-50 flex flex-col"
            initial={{ x: -256 }}
            animate={{ x: 0 }}
            exit={{ x: -256 }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
          >
            {/* Header */}
            <div className="p-6 border-b border-aurora-bg-tertiary flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-aurora-accent-cyan to-aurora-accent-blue flex items-center justify-center shadow-glow-cyan">
                  <Brain className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h1 className="text-lg font-bold gradient-text">AuroraSync</h1>
                  <p className="text-xs text-aurora-text-muted">OS v1.0</p>
                </div>
              </div>
              <button
                onClick={toggleSidebar}
                className="lg:hidden p-1 hover:bg-aurora-bg-hover rounded-lg transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Navigation */}
            <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
              {navItems.map((item) => (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={({ isActive }) =>
                    cn(
                      'flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200',
                      'hover:bg-aurora-bg-hover',
                      isActive
                        ? 'bg-aurora-accent-blue/20 text-aurora-accent-cyan border border-aurora-accent-blue/30 shadow-glow-blue'
                        : 'text-aurora-text-secondary hover:text-aurora-text-primary'
                    )
                  }
                  onClick={() => {
                    // Close sidebar on mobile after navigation
                    if (window.innerWidth < 1024) {
                      toggleSidebar()
                    }
                  }}
                >
                  <item.icon className="w-5 h-5" />
                  <span className="font-medium">{item.label}</span>
                </NavLink>
              ))}
            </nav>

            {/* Footer */}
            <div className="p-4 border-t border-aurora-bg-tertiary">
              <div className="glass rounded-lg p-3">
                <div className="flex items-center gap-2 mb-2">
                  <div className="w-2 h-2 rounded-full bg-aurora-status-healthy animate-pulse" />
                  <span className="text-sm font-medium">System Status</span>
                </div>
                <p className="text-xs text-aurora-text-muted">All systems operational</p>
              </div>
            </div>
          </motion.aside>
        )}
      </AnimatePresence>
    </>
  )
}

export default Sidebar
