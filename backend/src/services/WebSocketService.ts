import { WebSocketServer, WebSocket } from 'ws'
import { Server } from 'http'
import { sessionLauncher } from './SessionLauncher'
import { sessionMonitor } from './SessionMonitor'

export interface WSMessage {
  type: string
  data: any
  timestamp: string
}

export class WebSocketService {
  private wss: WebSocketServer | null = null
  private clients: Set<WebSocket> = new Set()

  /**
   * Initialize WebSocket server
   */
  initialize(server: Server) {
    this.wss = new WebSocketServer({ server, path: '/ws' })

    console.log('🔌 WebSocket server initialized on /ws')

    // Setup connection handling
    this.wss.on('connection', (ws: WebSocket) => {
      this.handleConnection(ws)
    })

    // Setup event listeners for session events
    this.setupEventListeners()
  }

  /**
   * Handle new WebSocket connection
   */
  private handleConnection(ws: WebSocket) {
    console.log('✅ New WebSocket client connected')

    // Add to clients set
    this.clients.add(ws)

    // Send welcome message
    this.sendToClient(ws, {
      type: 'connected',
      data: {
        message: 'Connected to Super Agent Monitor',
        activeSessions: sessionLauncher.getActiveSessions(),
        monitorStats: sessionMonitor.getStats()
      },
      timestamp: new Date().toISOString()
    })

    // Handle messages from client
    ws.on('message', (message: string) => {
      try {
        const data = JSON.parse(message.toString())
        this.handleClientMessage(ws, data)
      } catch (error) {
        console.error('Failed to parse client message:', error)
      }
    })

    // Handle client disconnect
    ws.on('close', () => {
      console.log('👋 WebSocket client disconnected')
      this.clients.delete(ws)
    })

    // Handle errors
    ws.on('error', (error) => {
      console.error('WebSocket error:', error)
      this.clients.delete(ws)
    })
  }

  /**
   * Handle message from client
   */
  private handleClientMessage(ws: WebSocket, message: any) {
    console.log('📨 Received message from client:', message.type)

    switch (message.type) {
      case 'ping':
        this.sendToClient(ws, {
          type: 'pong',
          data: { timestamp: new Date().toISOString() },
          timestamp: new Date().toISOString()
        })
        break

      case 'subscribe':
        // Client wants to subscribe to specific session
        const sessionId = message.data?.sessionId
        if (sessionId) {
          console.log(`📡 Client subscribed to session ${sessionId}`)
          // Store subscription info in client metadata
          (ws as any).subscriptions = (ws as any).subscriptions || []
          ;(ws as any).subscriptions.push(sessionId)
        }
        break

      case 'unsubscribe':
        // Client wants to unsubscribe from session
        const unsubSessionId = message.data?.sessionId
        if (unsubSessionId && (ws as any).subscriptions) {
          ;(ws as any).subscriptions = (ws as any).subscriptions.filter(
            (id: string) => id !== unsubSessionId
          )
          console.log(`📡 Client unsubscribed from session ${unsubSessionId}`)
        }
        break

      default:
        console.warn(`Unknown message type: ${message.type}`)
    }
  }

  /**
   * Setup event listeners for session and monitor events
   */
  private setupEventListeners() {
    // Session Launcher Events
    sessionLauncher.on('session:launched', (data) => {
      this.broadcast({
        type: 'session:launched',
        data,
        timestamp: new Date().toISOString()
      })
    })

    sessionLauncher.on('session:tool_use', (data) => {
      this.broadcastToSession(data.sessionId, {
        type: 'session:tool_use',
        data,
        timestamp: new Date().toISOString()
      })
    })

    sessionLauncher.on('session:error', (data) => {
      this.broadcastToSession(data.sessionId, {
        type: 'session:error',
        data,
        timestamp: new Date().toISOString()
      })
    })

    sessionLauncher.on('session:exit', (data) => {
      this.broadcast({
        type: 'session:exit',
        data,
        timestamp: new Date().toISOString()
      })
    })

    sessionLauncher.on('session:failed', (data) => {
      this.broadcast({
        type: 'session:failed',
        data,
        timestamp: new Date().toISOString()
      })
    })

    // Session Monitor Events
    sessionMonitor.on('session:stalled', (data) => {
      this.broadcast({
        type: 'session:stalled',
        data,
        timestamp: new Date().toISOString()
      })
    })

    sessionMonitor.on('session:restarted', (data) => {
      this.broadcast({
        type: 'session:restarted',
        data,
        timestamp: new Date().toISOString()
      })
    })

    sessionMonitor.on('session:restart_failed', (data) => {
      this.broadcast({
        type: 'session:restart_failed',
        data,
        timestamp: new Date().toISOString()
      })
    })

    sessionMonitor.on('monitor:started', () => {
      this.broadcast({
        type: 'monitor:started',
        data: sessionMonitor.getStats(),
        timestamp: new Date().toISOString()
      })
    })

    sessionMonitor.on('monitor:stopped', () => {
      this.broadcast({
        type: 'monitor:stopped',
        data: {},
        timestamp: new Date().toISOString()
      })
    })
  }

  /**
   * Broadcast message to all connected clients
   */
  broadcast(message: WSMessage) {
    const payload = JSON.stringify(message)

    this.clients.forEach((client) => {
      if (client.readyState === WebSocket.OPEN) {
        client.send(payload)
      }
    })

    console.log(`📢 Broadcast: ${message.type} to ${this.clients.size} clients`)
  }

  /**
   * Broadcast message to clients subscribed to a specific session
   */
  broadcastToSession(sessionId: string, message: WSMessage) {
    const payload = JSON.stringify(message)
    let sentCount = 0

    this.clients.forEach((client) => {
      if (client.readyState === WebSocket.OPEN) {
        const subscriptions = (client as any).subscriptions as string[] || []

        // Send to clients subscribed to this session or all sessions
        if (subscriptions.length === 0 || subscriptions.includes(sessionId)) {
          client.send(payload)
          sentCount++
        }
      }
    })

    console.log(`📢 Broadcast to session ${sessionId}: ${message.type} to ${sentCount} clients`)
  }

  /**
   * Send message to a specific client
   */
  private sendToClient(client: WebSocket, message: WSMessage) {
    if (client.readyState === WebSocket.OPEN) {
      client.send(JSON.stringify(message))
    }
  }

  /**
   * Get connected clients count
   */
  getClientCount(): number {
    return this.clients.size
  }

  /**
   * Shutdown WebSocket server
   */
  shutdown() {
    if (this.wss) {
      console.log('🔌 Shutting down WebSocket server')

      // Close all client connections
      this.clients.forEach((client) => {
        client.close(1000, 'Server shutting down')
      })

      // Close server
      this.wss.close()
      this.wss = null
    }
  }
}

// Singleton instance
export const webSocketService = new WebSocketService()
