import { motion } from 'framer-motion'
import { cn } from '@/utils/cn'

const Button = ({
  children,
  variant = 'primary',
  size = 'md',
  loading = false,
  disabled = false,
  className,
  icon,
  ...props
}) => {
  const variants = {
    primary: 'bg-aurora-accent-blue hover:bg-aurora-accent-cyan text-white shadow-glow-blue',
    secondary: 'bg-aurora-bg-tertiary hover:bg-aurora-bg-hover text-aurora-text-primary',
    danger: 'bg-aurora-accent-red hover:bg-red-600 text-white shadow-glow-red',
    success: 'bg-aurora-accent-green hover:bg-green-600 text-white shadow-glow-green',
    ghost: 'bg-transparent hover:bg-aurora-bg-tertiary text-aurora-text-primary',
    outline: 'bg-transparent border-2 border-aurora-accent-blue hover:bg-aurora-accent-blue/10 text-aurora-accent-blue',
  }

  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  }

  return (
    <motion.button
      className={cn(
        'inline-flex items-center justify-center gap-2 rounded-lg font-medium transition-all duration-200',
        'disabled:opacity-50 disabled:cursor-not-allowed',
        variants[variant],
        sizes[size],
        className
      )}
      disabled={disabled || loading}
      whileHover={{ scale: disabled || loading ? 1 : 1.02 }}
      whileTap={{ scale: disabled || loading ? 1 : 0.98 }}
      {...props}
    >
      {loading ? (
        <>
          <svg className="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Loading...
        </>
      ) : (
        <>
          {icon && <span>{icon}</span>}
          {children}
        </>
      )}
    </motion.button>
  )
}

export default Button
