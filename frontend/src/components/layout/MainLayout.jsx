import { motion } from 'framer-motion'
import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import TopBar from './TopBar'
import { useStore } from '@/store/useStore'
import { cn } from '@/utils/cn'

const MainLayout = () => {
  const { sidebarOpen } = useStore()

  return (
    <div className="min-h-screen bg-aurora-bg-primary">
      <Sidebar />
      <TopBar />
      
      <motion.main
        className={cn(
          'pt-16 min-h-screen transition-all duration-300',
          sidebarOpen ? 'lg:pl-64' : 'pl-0'
        )}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
      >
        <div className="p-6">
          <Outlet />
        </div>
      </motion.main>
    </div>
  )
}

export default MainLayout
