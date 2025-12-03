import axios from './axios'

export const voiceApi = {
  // Engage voice conversation
  engage: async (engageData) => {
    const response = await axios.post('/api/v1/voice/engage', engageData)
    return response.data
  },

  // Continue conversation
  continue: async (conversationId, userResponse) => {
    const response = await axios.post('/api/v1/voice/continue', {
      conversation_id: conversationId,
      user_response: userResponse
    })
    return response.data
  },

  // Transcribe audio
  transcribe: async (audioFile, language = 'en-IN') => {
    const formData = new FormData()
    formData.append('audio', audioFile)
    formData.append('language', language)
    
    const response = await axios.post('/api/v1/voice/transcribe', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  },

  // Get conversation
  getConversation: async (conversationId) => {
    const response = await axios.get(`/api/v1/voice/conversation/${conversationId}`)
    return response.data
  },

  // Get available voices
  getVoices: async () => {
    const response = await axios.get('/api/v1/voice/voices')
    return response.data
  },

  // Generate TTS
  generateTTS: async (text, voice = 'Aurora_Default', speakingRate = 1.0) => {
    const response = await axios.post('/api/v1/voice/tts', null, {
      params: { text, voice, speaking_rate: speakingRate }
    })
    return response.data
  },

  // Get audio
  getAudio: async (audioId) => {
    const response = await axios.get(`/api/v1/voice/audio/${audioId}`)
    return response.data
  },
}
