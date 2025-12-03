import { create } from 'zustand'

export const useStore = create((set, get) => ({
  // System state
  systemHealth: 'ok',
  setSystemHealth: (health) => set({ systemHealth: health }),

  // Vehicles
  vehicles: [],
  selectedVehicle: null,
  setVehicles: (vehicles) => set({ vehicles }),
  setSelectedVehicle: (vehicle) => set({ selectedVehicle: vehicle }),

  // Predictions
  predictions: [],
  setPredictions: (predictions) => set({ predictions }),
  addPrediction: (prediction) => set((state) => ({
    predictions: [prediction, ...state.predictions]
  })),

  // Agents
  agentStatus: null,
  setAgentStatus: (status) => set({ agentStatus: status }),

  // Workshops
  workshops: [],
  setWorkshops: (workshops) => set({ workshops }),

  // Conversations
  conversations: [],
  activeConversation: null,
  setConversations: (conversations) => set({ conversations }),
  setActiveConversation: (conversation) => set({ activeConversation: conversation }),
  addConversation: (conversation) => set((state) => ({
    conversations: [conversation, ...state.conversations]
  })),

  // UI state
  sidebarOpen: true,
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  
  loading: false,
  setLoading: (loading) => set({ loading }),

  // Notifications
  notifications: [],
  addNotification: (notification) => set((state) => ({
    notifications: [
      {
        id: Date.now(),
        timestamp: new Date().toISOString(),
        ...notification
      },
      ...state.notifications
    ].slice(0, 50) // Keep last 50
  })),
  clearNotifications: () => set({ notifications: [] }),
  removeNotification: (id) => set((state) => ({
    notifications: state.notifications.filter(n => n.id !== id)
  })),
}))
