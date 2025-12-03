import { motion } from 'framer-motion'
import { Menu, Bell, Search, User } from 'lucide-react'
import { useStore } from '@/store/useStore'
import { cn } from '@/utils/cn'

const TopBar = () => {
  const { toggleSidebar, notifications, sidebarOpen } = useStore()
  const unreadCount = notifications.filter(n => !n.read).length

  return (
    <motion.header
      className={cn(
        'fixed top-0 right-0 h-16 glass border-b border-aurora-bg-tertiary z-30 flex items-center justify-between px-6 transition-all duration-300',
        sidebarOpen ? 'left-64' : 'left-0'
      )}
      initial={{ y: -64 }}
      animate={{ y: 0 }}
      transition={{ type: 'spring', damping: 25, stiffness: 200 }}
    >
      {/* Left section */}
      <div className="flex items-center gap-4">
        <button
          onClick={toggleSidebar}
          className="p-2 hover:bg-aurora-bg-hover rounded-lg transition-colors"
        >
          <Menu className="w-5 h-5" />
        </button>

        {/* Search */}
        <div className="hidden md:flex items-center gap-2 bg-aurora-bg-tertiary rounded-lg px-4 py-2 w-64">
          <Search className="w-4 h-4 text-aurora-text-muted" />
          <input
            type="text"
            placeholder="Search vehicles, predictions..."
            className="bg-transparent border-none outline-none text-sm w-full text-aurora-text-primary placeholder-aurora-text-muted"
          />
        </div>
      </div>

      {/* Right section */}
      <div className="flex items-center gap-4">
        {/* Notifications */}
        <button className="relative p-2 hover:bg-aurora-bg-hover rounded-lg transition-colors">
          <Bell className="w-5 h-5" />
          {unreadCount > 0 && (
            <motion.span
              className="absolute -top-1 -right-1 w-5 h-5 bg-aurora-accent-red rounded-full text-xs flex items-center justify-center text-white font-bold"
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ type: 'spring', stiffness: 500, damping: 15 }}
            >
              {unreadCount > 9 ? '9+' : unreadCount}
            </motion.span>
          )}
        </button>

        {/* User profile */}
        <div className="flex items-center gap-3 pl-4 border-l border-aurora-bg-tertiary">
          <div className="hidden md:block text-right">
            <p className="text-sm font-medium">Admin User</p>
            <p className="text-xs text-aurora-text-muted">System Administrator</p>
          </div>
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-aurora-accent-purple to-aurora-accent-pink flex items-center justify-center shadow-glow-purple">
            <User className="w-5 h-5 text-white" />
          </div>
        </div>
      </div>
    </motion.header>
  )
}

export default TopBar
