import { ref, onMounted, onUnmounted } from 'vue'

export interface WSMessage {
  type: string
  data: any
  timestamp: string
}

export interface UseWebSocketOptions {
  url: string
  reconnect?: boolean
  reconnectInterval?: number
  onMessage?: (message: WSMessage) => void
  onError?: (error: Event) => void
  onConnect?: () => void
  onDisconnect?: () => void
}

export function useWebSocket(options: UseWebSocketOptions) {
  const {
    url,
    reconnect = true,
    reconnectInterval = 5000,
    onMessage,
    onError,
    onConnect,
    onDisconnect
  } = options

  const ws = ref<WebSocket | null>(null)
  const isConnected = ref(false)
  const lastMessage = ref<WSMessage | null>(null)
  const reconnectTimer = ref<number | null>(null)

  const connect = () => {
    try {
      // Determine WebSocket URL
      const wsUrl = url.startsWith('ws://') || url.startsWith('wss://')
        ? url
        : `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${window.location.host}${url}`

      ws.value = new WebSocket(wsUrl)

      ws.value.onopen = () => {
        console.log('WebSocket connected')
        isConnected.value = true
        onConnect?.()
      }

      ws.value.onmessage = (event) => {
        try {
          const message: WSMessage = JSON.parse(event.data)
          lastMessage.value = message
          onMessage?.(message)
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error)
        }
      }

      ws.value.onerror = (error) => {
        console.error('WebSocket error:', error)
        onError?.(error)
      }

      ws.value.onclose = () => {
        console.log('WebSocket disconnected')
        isConnected.value = false
        ws.value = null
        onDisconnect?.()

        // Auto-reconnect
        if (reconnect && !reconnectTimer.value) {
          reconnectTimer.value = window.setTimeout(() => {
            reconnectTimer.value = null
            connect()
          }, reconnectInterval)
        }
      }
    } catch (error) {
      console.error('Failed to create WebSocket connection:', error)
    }
  }

  const disconnect = () => {
    if (reconnectTimer.value) {
      clearTimeout(reconnectTimer.value)
      reconnectTimer.value = null
    }

    if (ws.value) {
      ws.value.close()
      ws.value = null
    }

    isConnected.value = false
  }

  const send = (message: any) => {
    if (ws.value && isConnected.value) {
      ws.value.send(JSON.stringify(message))
    } else {
      console.warn('WebSocket is not connected')
    }
  }

  const subscribe = (sessionId: string) => {
    send({ action: 'subscribe', sessionId })
  }

  const unsubscribe = (sessionId: string) => {
    send({ action: 'unsubscribe', sessionId })
  }

  onMounted(() => {
    connect()
  })

  onUnmounted(() => {
    disconnect()
  })

  return {
    ws,
    isConnected,
    lastMessage,
    connect,
    disconnect,
    send,
    subscribe,
    unsubscribe
  }
}
