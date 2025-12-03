import { motion } from 'framer-motion'
import { User, Bot, Volume2, Loader2 } from 'lucide-react'
import { cn } from '@/utils/cn'
import { formatDate } from '@/utils/formatters'

const VoiceConversationBubble = ({ message, className }) => {
  const { role, content, timestamp, audio_url, is_loading } = message
  const isUser = role === 'user'

  const handlePlayAudio = () => {
    if (audio_url) {
      const audio = new Audio(audio_url)
      audio.play()
    }
  }

  return (
    <motion.div
      className={cn(
        'flex gap-3 mb-4',
        isUser ? 'flex-row-reverse' : 'flex-row',
        className
      )}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      {/* Avatar */}
      <div className={cn(
        'w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0',
        isUser 
          ? 'bg-aurora-accent-purple/20 border border-aurora-accent-purple/30' 
          : 'bg-gradient-to-br from-aurora-accent-cyan to-aurora-accent-blue shadow-glow-cyan'
      )}>
        {isUser ? (
          <User className="w-5 h-5 text-aurora-accent-purple" />
        ) : (
          <Bot className="w-5 h-5 text-white" />
        )}
      </div>

      {/* Message Content */}
      <div className={cn(
        'flex-1 max-w-[70%]',
        isUser ? 'items-end' : 'items-start'
      )}>
        <div className={cn(
          'rounded-2xl px-4 py-3',
          isUser 
            ? 'bg-aurora-accent-purple/20 border border-aurora-accent-purple/30' 
            : 'glass border border-aurora-bg-tertiary'
        )}>
          {is_loading ? (
            <div className="flex items-center gap-2">
              <Loader2 className="w-4 h-4 animate-spin text-aurora-accent-cyan" />
              <span className="text-sm text-aurora-text-muted">Processing...</span>
            </div>
          ) : (
            <>
              <p className="text-sm text-aurora-text-primary whitespace-pre-wrap">
                {content}
              </p>
              
              {/* Audio Player */}
              {audio_url && !isUser && (
                <button
                  onClick={handlePlayAudio}
                  className="mt-2 flex items-center gap-2 px-3 py-1.5 bg-aurora-bg-tertiary hover:bg-aurora-bg-hover rounded-lg transition-colors"
                >
                  <Volume2 className="w-4 h-4 text-aurora-accent-cyan" />
                  <span className="text-xs text-aurora-text-secondary">Play Audio</span>
                </button>
              )}
            </>
          )}
        </div>

        {/* Timestamp */}
        {timestamp && !is_loading && (
          <p className={cn(
            'text-xs text-aurora-text-muted mt-1 px-2',
            isUser ? 'text-right' : 'text-left'
          )}>
            {formatDate(timestamp)}
          </p>
        )}
      </div>
    </motion.div>
  )
}

export default VoiceConversationBubble
