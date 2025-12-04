import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Mic, Send, User, Bot, Volume2 } from 'lucide-react'
import Card from '@/components/ui/Card'
import Button from '@/components/ui/Button'
import VoiceConversationBubble from '@/components/VoiceConversationBubble'
import { voiceApi } from '@/api/voice'
import { formatRelativeTime } from '@/utils/formatters'
import toast from 'react-hot-toast'

const VoiceAI = () => {
  const [loading, setLoading] = useState(false)
  const [conversation, setConversation] = useState(null)
  const [messages, setMessages] = useState([])
  const [userInput, setUserInput] = useState('')
  const [scenario, setScenario] = useState('predicted_failure')

  useEffect(() => {
    document.title = 'Aurora - Your AI Companion | AuroraSync OS'
    return () => {
      document.title = 'AuroraSync OS | The Self-Healing Vehicle Brain'
    }
  }, [])

  const scenarios = [
    { value: 'predicted_failure', label: '🔮 Crystal Ball - Predict & Prevent', icon: '🔮' },
    { value: 'urgent_alert', label: '🚨 Red Alert - Critical Response', icon: '🚨' },
    { value: 'appointment_reminder', label: '⏰ Time Keeper - Friendly Nudge', icon: '⏰' },
    { value: 'post_service_feedback', label: '⭐ Feedback Loop - Quality Check', icon: '⭐' },
    { value: 'booking_recovery', label: '🎯 Second Chance - Win Back', icon: '🎯' },
  ]

  const handleStartConversation = async () => {
    try {
      setLoading(true)
      
      // Use mock conversation directly for reliable demo
      const mockMessages = {
        'predicted_failure': '🔮 Namaste Rahul! This is Aurora, your vehicle\'s guardian angel. My crystal ball (aka AI sensors) detected your Honda Accord\'s brake system needs some TLC soon. The failure probability is 85% - not great odds! Can I book a service appointment for you tomorrow at 10 AM at AutoCare Mumbai? Let\'s prevent this before it becomes a problem!',
        'urgent_alert': '🚨 RED ALERT! Rahul, this is Aurora with an urgent message about your Honda Accord. We\'ve detected a critical issue that needs immediate attention. Think of me as your vehicle\'s emergency hotline - please bring it to AutoCare Mumbai ASAP. Your safety is our priority!',
        'appointment_reminder': '⏰ Hi Rahul! Your friendly neighborhood reminder bot here! Just checking in about your service appointment tomorrow at 10 AM at AutoCare Mumbai for your Honda Accord. Will you be able to make it? I promise we\'ll have chai ready for you!',
        'post_service_feedback': '⭐ Hello Rahul! Aurora here, doing my quality check rounds. Thank you for servicing your Honda Accord at AutoCare Mumbai. How was your experience? Your feedback helps us get better - think of it as teaching an AI to be more awesome!',
        'booking_recovery': '🎯 Hi Rahul! Aurora again - I noticed you declined the service appointment. No worries, life happens! Is there a better time that works for you? We want to ensure your Honda Accord stays in great condition. Let\'s find a slot that fits your schedule!'
      }
      
      setConversation({
        conversation_id: 'mock-' + Date.now(),
        status: 'active',
        scenario: scenario
      })
      
      setMessages([{
        role: 'assistant',
        content: mockMessages[scenario] || mockMessages['predicted_failure'],
        timestamp: new Date().toISOString(),
        audio: null
      }])
      
      toast.success('Conversation started')
    } finally {
      setLoading(false)
    }
  }

  const handleSendMessage = async () => {
    if (!userInput.trim() || !conversation) return

    const userMessage = {
      role: 'user',
      content: userInput,
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])
    const currentInput = userInput
    setUserInput('')

    try {
      setLoading(true)
      
      // Use mock response directly for reliable demo
      const mockResponses = {
        'yes': '🎉 Awesome! Your appointment is locked in for tomorrow at 10 AM at AutoCare Mumbai. You\'ll get a confirmation SMS faster than you can say "predictive maintenance"! Anything else I can help you with today?',
        'no': '😊 No worries, I get it! Life gets busy. Would you like me to suggest some alternative times? We have slots available throughout the week - I\'m like a calendar ninja, I\'ll find something that works!',
        'reschedule': '📅 Absolutely! Let\'s find a time that works better for you. We have availability throughout the week. Morning person? Night owl? Weekend warrior? I\'ve got options for everyone!',
        'more': '🔍 Here\'s the technical scoop: Your brake pads are worn down to 2mm (that\'s critical level - think of it as your brakes running on fumes). If we don\'t fix this soon, you might experience brake failure. The service takes about 2 hours and costs approximately ₹5,000. Think of it as an investment in not crashing!',
        'options': '🎯 You\'ve got choices! 1) Lock in tomorrow at 10 AM (the early bird special), 2) Pick a different time this week (we\'re flexible like yoga instructors), 3) Get a callback from our service advisor (the human touch). What sounds good to you?'
      }
      
      let response = '👍 Got it! Thanks for chatting with me. Our team will follow up with you shortly. In the meantime, is there anything else I can help you with today? I\'m here all day (perks of being an AI)!'
      
      const lowerInput = currentInput.toLowerCase()
      if (lowerInput.includes('yes') || lowerInput.includes('book')) {
        response = mockResponses['yes']
      } else if (lowerInput.includes('no') || lowerInput.includes('not')) {
        response = mockResponses['no']
      } else if (lowerInput.includes('reschedule') || lowerInput.includes('different')) {
        response = mockResponses['reschedule']
      } else if (lowerInput.includes('more') || lowerInput.includes('tell')) {
        response = mockResponses['more']
      } else if (lowerInput.includes('option')) {
        response = mockResponses['options']
      }
      
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response,
        timestamp: new Date().toISOString(),
        audio: null
      }])
    } finally {
      setLoading(false)
    }
  }

  const handlePlayAudio = (audioId) => {
    toast.success('Audio playback simulated (TTS integration required)')
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-3xl font-bold gradient-text mb-2">🌟 Aurora - Your AI Companion</h1>
        <p className="text-aurora-text-secondary">
          Your vehicle's guardian angel • Intelligent conversations powered by predictive AI
        </p>
        <div className="mt-2 px-4 py-2 bg-aurora-accent-purple/10 border border-aurora-accent-purple/30 rounded-lg">
          <p className="text-sm text-aurora-text-secondary">
            ✨ <span className="text-aurora-accent-cyan font-medium">Meet Aurora:</span> Not your average AI - she's got personality, empathy, and a knack for keeping your vehicle healthy. 
            In production, Aurora makes voice calls using Text-to-Speech for that human touch.
          </p>
        </div>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Configuration */}
        <Card>
          <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
            <Mic className="w-5 h-5 text-aurora-accent-purple" />
            Configuration
          </h2>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Scenario</label>
              <select
                value={scenario}
                onChange={(e) => setScenario(e.target.value)}
                className="input"
                disabled={conversation !== null}
              >
                {scenarios.map(s => (
                  <option key={s.value} value={s.value}>{s.label}</option>
                ))}
              </select>
            </div>

            <Button
              variant="primary"
              className="w-full"
              onClick={handleStartConversation}
              loading={loading}
              disabled={conversation !== null}
              icon={<Mic className="w-4 h-4" />}
            >
              Start Conversation
            </Button>

            {conversation && (
              <Button
                variant="secondary"
                className="w-full"
                onClick={() => {
                  setConversation(null)
                  setMessages([])
                }}
              >
                Reset
              </Button>
            )}
          </div>

          {/* Conversation Info */}
          {conversation && (
            <div className="mt-6 glass rounded-lg p-4">
              <h3 className="font-medium mb-3">Conversation Info</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-aurora-text-muted">ID</span>
                  <span className="font-mono text-xs">{conversation.conversation_id}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-aurora-text-muted">Status</span>
                  <span className="font-medium">{conversation.status}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-aurora-text-muted">Messages</span>
                  <span className="font-medium">{messages.length}</span>
                </div>
              </div>
            </div>
          )}
        </Card>

        {/* Conversation */}
        <Card className="lg:col-span-2">
          <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
            <Bot className="w-5 h-5 text-aurora-accent-cyan" />
            Conversation
          </h2>

          {/* Messages */}
          <div className="space-y-2 mb-4 h-[500px] overflow-y-auto">
            {messages.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-full text-center">
                <Mic className="w-16 h-16 text-aurora-text-muted mb-4" />
                <p className="text-aurora-text-muted">
                  Select a scenario and start a conversation
                </p>
              </div>
            ) : (
              messages.map((message, index) => (
                <VoiceConversationBubble
                  key={index}
                  message={{
                    role: message.role,
                    content: message.content,
                    timestamp: message.timestamp,
                    audio_url: message.audio?.audio_url,
                    is_loading: false
                  }}
                />
              ))
            )}
            {loading && (
              <VoiceConversationBubble
                message={{
                  role: 'assistant',
                  content: '',
                  is_loading: true
                }}
              />
            )}
          </div>

          {/* Input */}
          {conversation && (
            <div className="flex gap-3">
              <input
                type="text"
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                placeholder="Type your response..."
                className="input flex-1"
                disabled={loading}
              />
              <Button
                variant="primary"
                onClick={handleSendMessage}
                loading={loading}
                disabled={!userInput.trim()}
                icon={<Send className="w-4 h-4" />}
              >
                Send
              </Button>
            </div>
          )}
        </Card>
      </div>

      {/* Quick Responses */}
      {conversation && (
        <Card>
          <h3 className="font-medium mb-4">Quick Responses</h3>
          <div className="flex flex-wrap gap-2">
            {[
              'Yes, please book it',
              'No, not now',
              'Can we reschedule?',
              'Tell me more',
              'What are my options?'
            ].map((response) => (
              <Button
                key={response}
                variant="ghost"
                size="sm"
                onClick={() => {
                  setUserInput(response)
                }}
                disabled={loading}
              >
                {response}
              </Button>
            ))}
          </div>
        </Card>
      )}
    </div>
  )
}

export default VoiceAI
