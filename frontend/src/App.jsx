import { useState, useEffect } from 'react'
import { Shield, AlertCircle, CheckCircle, Activity, Brain, Zap, Clock, Wifi } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

function App() {
  const [status, setStatus] = useState('idle')
  const [events, setEvents] = useState([])
  const [summary, setSummary] = useState('')
  const [systemStatus, setSystemStatus] = useState(null)
  const [lastEvent, setLastEvent] = useState(null)
  const [loading, setLoading] = useState(false)
  const [activeStep, setActiveStep] = useState(0)

  // Fetch initial events and status, then poll every 5 seconds as fallback
  useEffect(() => {
    fetchEvents()
    fetchSystemStatus()
    
    // Polling fallback every 5 seconds (in case SSE fails)
    const pollInterval = setInterval(() => {
      fetchEvents()
    }, 5000)
    
    return () => clearInterval(pollInterval)
  }, [])

  // Animate system flow when event occurs
  const animateFlow = () => {
    // Animate through all 5 steps
    setActiveStep(1)
    setTimeout(() => setActiveStep(2), 200)
    setTimeout(() => setActiveStep(3), 400)
    setTimeout(() => setActiveStep(4), 600)
    setTimeout(() => setActiveStep(5), 800)
    setTimeout(() => setActiveStep(0), 1500) // Reset
  }

  // Set up SSE connection for real-time updates with auto-reconnect
  useEffect(() => {
    let eventSource = null
    let reconnectTimeout = null
    
    const connectSSE = () => {
      console.log('🔌 Connecting to SSE stream...')
      eventSource = new EventSource(`${API_BASE_URL}/api/events/stream`)
      
      eventSource.onopen = () => {
        console.log('✅ SSE connected')
      }
      
      eventSource.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          console.log('📡 SSE received:', data)
          setLastEvent(data)
          setEvents(prev => [data, ...prev].slice(0, 20))
          
          // Update status based on event type
          if (data.type === 'alert') {
            // Animate system flow for Arduino ALERTS
            animateFlow()
            setStatus('alert')
            setTimeout(() => setStatus('idle'), 5000)
          } else if (data.type === 'checkin') {
            // Animate system flow for Arduino CHECK-INS too
            animateFlow()
            setStatus('safe')
            setTimeout(() => setStatus('idle'), 3000)
          } else if (data.type === 'omi_transcript') {
            // OMI transcripts don't trigger system flow animation (not from Arduino)
            // Only update status if distress is detected (don't show 'safe' during active alert)
            if (data.distress_detected) {
              setStatus('alert')
              setTimeout(() => setStatus('idle'), 5000)
            }
            // Non-distress transcripts during alert don't change status
          } else if (data.type === 'alert_resolved') {
            // Alert resolved via triple-tap
            setStatus('safe')
            setTimeout(() => setStatus('idle'), 3000)
          }
        } catch (err) {
          console.error('SSE parse error:', err)
        }
      }

      eventSource.onerror = (err) => {
        console.error('❌ SSE error:', err)
        eventSource.close()
        
        // Auto-reconnect after 3 seconds
        console.log('🔄 SSE reconnecting in 3 seconds...')
        reconnectTimeout = setTimeout(connectSSE, 3000)
      }
    }
    
    connectSSE()

    return () => {
      if (eventSource) eventSource.close()
      if (reconnectTimeout) clearTimeout(reconnectTimeout)
    }
  }, [])

  const fetchEvents = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/events`)
      const data = await response.json()
      setEvents(data.events || [])
    } catch (err) {
      console.error('Error fetching events:', err)
    }
  }

  const fetchSystemStatus = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/status`)
      const data = await response.json()
      setSystemStatus(data)
    } catch (err) {
      console.error('Error fetching status:', err)
    }
  }

  const fetchSummary = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/api/summary`)
      const data = await response.json()
      setSummary(data.summary)
    } catch (err) {
      console.error('Error fetching summary:', err)
      setSummary('Error generating summary')
    } finally {
      setLoading(false)
    }
  }

  const simulateCheckin = async () => {
    try {
      await fetch(`${API_BASE_URL}/api/checkin`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
      })
    } catch (err) {
      console.error('Error simulating check-in:', err)
    }
  }

  const simulateAlert = async () => {
    try {
      await fetch(`${API_BASE_URL}/api/alert`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ description: 'Demo alert triggered' })
      })
    } catch (err) {
      console.error('Error simulating alert:', err)
    }
  }

  const getStatusColor = () => {
    switch (status) {
      case 'alert': return 'bg-red-500'
      case 'safe': return 'bg-green-500'
      default: return 'bg-blue-500'
    }
  }

  const getStatusText = () => {
    switch (status) {
      case 'alert': return 'ALERT TRIGGERED'
      case 'safe': return 'Safe - Checked In'
      default: return 'System Active'
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 text-white">
      {/* Header */}
      <header className="border-b border-white/10 backdrop-blur-sm bg-white/5">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Shield className="w-8 h-8 text-blue-400" />
            <div>
              <h1 className="text-2xl font-bold">Guardian Angel AI</h1>
              <p className="text-sm text-gray-400">Personal Safety Monitor</p>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            {systemStatus && (
              <div className="flex items-center gap-2 text-sm">
                <Wifi className={`w-4 h-4 ${systemStatus.status === 'online' ? 'text-green-400' : 'text-red-400'}`} />
                <span className="text-gray-300">{systemStatus.total_events} Events</span>
              </div>
            )}
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Status Card */}
          <div className="lg:col-span-2">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className={`rounded-2xl p-8 ${getStatusColor()} ${status === 'alert' ? 'animate-alert-pulse' : ''} shadow-2xl`}
            >
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  {status === 'alert' ? (
                    <AlertCircle className="w-12 h-12 animate-pulse" />
                  ) : status === 'safe' ? (
                    <CheckCircle className="w-12 h-12" />
                  ) : (
                    <Shield className="w-12 h-12" />
                  )}
                  <div>
                    <h2 className="text-3xl font-bold">{getStatusText()}</h2>
                    {lastEvent && (
                      <p className="text-sm opacity-90 mt-1 flex items-center gap-2">
                        <Clock className="w-4 h-4" />
                        {new Date(lastEvent.timestamp).toLocaleTimeString()}
                      </p>
                    )}
                  </div>
                </div>
              </div>
              
              {lastEvent && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="mt-4 p-4 bg-black/20 rounded-lg"
                >
                  <p className="text-sm">{lastEvent.message}</p>
                </motion.div>
              )}
            </motion.div>

            {/* Event Timeline */}
            <div className="mt-6 bg-slate-800/50 backdrop-blur-sm rounded-2xl p-6 border border-white/10">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-semibold flex items-center gap-2">
                  <Activity className="w-5 h-5 text-blue-400" />
                  Event Timeline
                </h3>
              </div>
              
              <div className="space-y-3 max-h-96 overflow-y-auto">
                <AnimatePresence>
                  {events.length === 0 ? (
                    <p className="text-gray-400 text-center py-8">No events recorded yet</p>
                  ) : (
                    events.map((event) => (
                      <motion.div
                        key={event.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: 20 }}
                        className={`flex items-start gap-3 p-3 rounded-lg ${
                          event.type === 'alert' 
                            ? 'bg-red-500/10 border border-red-500/20' 
                            : event.type === 'omi_transcript'
                            ? event.distress_detected
                              ? 'bg-orange-500/10 border border-orange-500/20'
                              : 'bg-purple-500/10 border border-purple-500/20'
                            : 'bg-green-500/10 border border-green-500/20'
                        }`}
                      >
                        {event.type === 'alert' ? (
                          <AlertCircle className="w-5 h-5 text-red-400 mt-0.5" />
                        ) : event.type === 'omi_transcript' ? (
                          <Activity className={`w-5 h-5 mt-0.5 ${event.distress_detected ? 'text-orange-400' : 'text-purple-400'}`} />
                        ) : (
                          <CheckCircle className="w-5 h-5 text-green-400 mt-0.5" />
                        )}
                        <div className="flex-1">
                          <div className="flex items-center justify-between">
                            <span className="font-medium">
                              {event.type === 'alert' ? 'Alert' : event.type === 'omi_transcript' ? '🎤 OMI Transcript' : 'Check-in'}
                              {event.type === 'omi_transcript' && event.distress_detected && (
                                <span className="ml-2 text-xs bg-orange-500/20 text-orange-400 px-2 py-0.5 rounded">⚠️ DISTRESS</span>
                              )}
                            </span>
                            <span className="text-xs text-gray-400">
                              {new Date(event.timestamp).toLocaleString()}
                            </span>
                          </div>
                          {event.type === 'omi_transcript' ? (
                            <div className="mt-1">
                              <p className="text-sm text-gray-300 italic">"{event.transcript || 'No transcript'}"</p>
                              {event.uid && <p className="text-xs text-gray-500 mt-1">Session: {event.session_id || 'N/A'}</p>}
                            </div>
                          ) : (
                            <p className="text-sm text-gray-300 mt-1">{event.message}</p>
                          )}
                        </div>
                      </motion.div>
                    ))
                  )}
                </AnimatePresence>
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* AI Summary Card */}
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-6 border border-white/10">
              <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Brain className="w-5 h-5 text-purple-400" />
                AI Summary
              </h3>
              
              <button
                onClick={fetchSummary}
                disabled={loading}
                className="w-full bg-purple-600 hover:bg-purple-700 disabled:bg-purple-800 disabled:cursor-not-allowed px-4 py-3 rounded-lg font-medium transition-colors flex items-center justify-center gap-2 mb-4"
              >
                {loading ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Generating...
                  </>
                ) : (
                  <>
                    <Zap className="w-4 h-4" />
                    Generate Summary
                  </>
                )}
              </button>
              
              {summary && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="p-4 bg-purple-500/10 border border-purple-500/20 rounded-lg"
                >
                  <p className="text-sm text-gray-200">{summary}</p>
                </motion.div>
              )}
            </div>

            {/* System Architecture */}
            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-6 border border-blue-500/30 shadow-lg">
              <h3 className="text-xl font-bold mb-4 text-white flex items-center gap-2">
                <Activity className="w-5 h-5 text-blue-400" />
                System Flow
                {activeStep > 0 && (
                  <span className="ml-auto text-xs text-green-400 animate-pulse">● ACTIVE</span>
                )}
              </h3>
              <div className="space-y-2">
                <motion.div 
                  animate={activeStep === 1 ? { scale: 1.05 } : { scale: 1 }}
                  className={`flex items-center gap-3 p-2 rounded-lg transition-all ${activeStep === 1 ? 'bg-blue-500/30 shadow-lg' : 'hover:bg-blue-500/10'}`}
                >
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center shadow-lg transition-all ${activeStep === 1 ? 'bg-blue-400 animate-pulse ring-4 ring-blue-400/50' : 'bg-blue-500'}`}>
                    <span className="text-white font-bold">1</span>
                  </div>
                  <div className="flex-1">
                    <span className="text-white font-medium block">Touch Sensor</span>
                    <span className="text-gray-400 text-xs">Physical input</span>
                  </div>
                  {activeStep === 1 && <Zap className="w-4 h-4 text-yellow-400 animate-pulse" />}
                </motion.div>
                <div className={`ml-5 border-l-2 h-4 transition-colors ${activeStep >= 2 ? 'border-blue-400 animate-pulse' : 'border-blue-400/50'}`}></div>
                
                <motion.div 
                  animate={activeStep === 2 ? { scale: 1.05 } : { scale: 1 }}
                  className={`flex items-center gap-3 p-2 rounded-lg transition-all ${activeStep === 2 ? 'bg-blue-500/30 shadow-lg' : 'hover:bg-blue-500/10'}`}
                >
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center shadow-lg transition-all ${activeStep === 2 ? 'bg-blue-400 animate-pulse ring-4 ring-blue-400/50' : 'bg-blue-500'}`}>
                    <span className="text-white font-bold">2</span>
                  </div>
                  <div className="flex-1">
                    <span className="text-white font-medium block">Arduino R4 WiFi</span>
                    <span className="text-gray-400 text-xs">IoT controller</span>
                  </div>
                  {activeStep === 2 && <Zap className="w-4 h-4 text-yellow-400 animate-pulse" />}
                </motion.div>
                <div className={`ml-5 border-l-2 h-4 transition-colors ${activeStep >= 3 ? 'border-purple-400 animate-pulse' : 'border-blue-400/50'}`}></div>
                
                <motion.div 
                  animate={activeStep === 3 ? { scale: 1.05 } : { scale: 1 }}
                  className={`flex items-center gap-3 p-2 rounded-lg transition-all ${activeStep === 3 ? 'bg-purple-500/30 shadow-lg' : 'hover:bg-purple-500/10'}`}
                >
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center shadow-lg transition-all ${activeStep === 3 ? 'bg-purple-400 animate-pulse ring-4 ring-purple-400/50' : 'bg-purple-500'}`}>
                    <span className="text-white font-bold">3</span>
                  </div>
                  <div className="flex-1">
                    <span className="text-white font-medium block">Flask Backend</span>
                    <span className="text-gray-400 text-xs">API server</span>
                  </div>
                  {activeStep === 3 && <Zap className="w-4 h-4 text-yellow-400 animate-pulse" />}
                </motion.div>
                <div className={`ml-5 border-l-2 h-4 transition-colors ${activeStep >= 4 ? 'border-purple-400 animate-pulse' : 'border-purple-400/50'}`}></div>
                
                <motion.div 
                  animate={activeStep === 4 ? { scale: 1.05 } : { scale: 1 }}
                  className={`flex items-center gap-3 p-2 rounded-lg transition-all ${activeStep === 4 ? 'bg-purple-500/30 shadow-lg' : 'hover:bg-purple-500/10'}`}
                >
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center shadow-lg transition-all ${activeStep === 4 ? 'bg-purple-400 animate-pulse ring-4 ring-purple-400/50' : 'bg-purple-500'}`}>
                    <span className="text-white font-bold">4</span>
                  </div>
                  <div className="flex-1">
                    <span className="text-white font-medium block">ChromaDB</span>
                    <span className="text-gray-400 text-xs">Vector storage</span>
                  </div>
                  {activeStep === 4 && <Zap className="w-4 h-4 text-yellow-400 animate-pulse" />}
                </motion.div>
                <div className={`ml-5 border-l-2 h-4 transition-colors ${activeStep >= 5 ? 'border-purple-400 animate-pulse' : 'border-purple-400/50'}`}></div>
                
                <motion.div 
                  animate={activeStep === 5 ? { scale: 1.05 } : { scale: 1 }}
                  className={`flex items-center gap-3 p-2 rounded-lg transition-all ${activeStep === 5 ? 'bg-purple-500/30 shadow-lg' : 'hover:bg-purple-500/10'}`}
                >
                  <div className={`w-10 h-10 rounded-full flex items-center justify-center shadow-lg transition-all ${activeStep === 5 ? 'bg-purple-400 animate-pulse ring-4 ring-purple-400/50' : 'bg-purple-600'}`}>
                    <span className="text-white font-bold">5</span>
                  </div>
                  <div className="flex-1">
                    <span className="text-white font-medium block">AI Analysis</span>
                    <span className="text-gray-400 text-xs">Smart summaries</span>
                  </div>
                  {activeStep === 5 && <Zap className="w-4 h-4 text-yellow-400 animate-pulse" />}
                </motion.div>
              </div>
            </div>

            {/* Demo Controls */}
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-6 border border-white/10">
              <h3 className="text-xl font-semibold mb-4">Demo Controls</h3>
              <div className="space-y-3">
                <button
                  onClick={simulateCheckin}
                  className="w-full bg-green-600 hover:bg-green-700 px-4 py-3 rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
                >
                  <CheckCircle className="w-4 h-4" />
                  Simulate Check-in
                </button>
                <button
                  onClick={simulateAlert}
                  className="w-full bg-red-600 hover:bg-red-700 px-4 py-3 rounded-lg font-medium transition-colors flex items-center justify-center gap-2"
                >
                  <AlertCircle className="w-4 h-4" />
                  Simulate Alert
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
