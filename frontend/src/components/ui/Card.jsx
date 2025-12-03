import { motion } from 'framer-motion'
import { cn } from '@/utils/cn'

const Card = ({ 
  children, 
  className, 
  hover = false, 
  glow = false,
  glowColor = 'blue',
  animated = true,
  onClick,
  ...props 
}) => {
  const Component = animated ? motion.div : 'div'
  
  const glowClasses = {
    blue: 'hover:shadow-glow-blue hover:border-aurora-accent-blue/50',
    cyan: 'hover:shadow-glow-cyan hover:border-aurora-accent-cyan/50',
    green: 'hover:shadow-glow-green hover:border-aurora-accent-green/50',
    red: 'hover:shadow-glow-red hover:border-aurora-accent-red/50',
    purple: 'hover:shadow-glow-purple hover:border-aurora-accent-purple/50',
  }

  return (
    <Component
      className={cn(
        'glass rounded-xl p-6 shadow-lg',
        hover && 'hover:bg-aurora-bg-hover/60 transition-all duration-300 cursor-pointer',
        glow && glowClasses[glowColor],
        onClick && 'cursor-pointer',
        className
      )}
      onClick={onClick}
      {...(animated && {
        initial: { opacity: 0, y: 20 },
        animate: { opacity: 1, y: 0 },
        transition: { duration: 0.3 }
      })}
      {...props}
    >
      {children}
    </Component>
  )
}

export default Card
