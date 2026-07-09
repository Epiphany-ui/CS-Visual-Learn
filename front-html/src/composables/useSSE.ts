import type { SSETaskEvent, SSEDoneEvent } from '@/types/api'

type SSECallback = (data: SSETaskEvent | SSEDoneEvent) => void

export function useSSE() {
  let eventSource: EventSource | null = null

  function connect(taskId: string, onMessage: SSECallback, onError?: (err: Event) => void) {
    disconnect()
    const url = `http://localhost:8000/api/tasks/${taskId}/stream`
    eventSource = new EventSource(url)

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        onMessage(data)
      } catch (e) {
        console.warn('SSE parse error:', e)
      }
    }

    eventSource.onerror = (err) => {
      console.error('SSE error:', err)
      onError?.(err)
      disconnect()
    }
  }

  function disconnect() {
    if (eventSource) {
      eventSource.close()
      eventSource = null
    }
  }

  return { connect, disconnect }
}
