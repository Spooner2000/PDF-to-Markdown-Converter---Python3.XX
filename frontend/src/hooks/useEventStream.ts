import { useEffect, useRef, useState } from 'react';
import { getBackendBaseUrl } from '../services/api';

type EventEnvelope = {
  id: string;
  type: string;
  payload: Record<string, unknown>;
  timestamp: string;
};

type StreamState = 'idle' | 'connecting' | 'open' | 'closed' | 'error';

export function useEventStream(active: boolean) {
  const [events, setEvents] = useState<EventEnvelope[]>([]);
  const [state, setState] = useState<StreamState>('idle');
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!active) {
      wsRef.current?.close();
      setState('closed');
      return;
    }

    let mounted = true;
    const connect = async () => {
      setState('connecting');
      try {
        const baseUrl = await getBackendBaseUrl();
        const wsUrl = baseUrl.replace('http', 'ws').replace(/\/$/, '') + '/ws/events';
        const socket = new WebSocket(wsUrl);
        wsRef.current = socket;

        socket.onopen = () => {
          if (!mounted) return;
          setState('open');
        };

        socket.onmessage = (event) => {
          try {
            const payload = JSON.parse(event.data) as EventEnvelope;
            setEvents((prev) => {
              const next = [...prev, payload];
              return next.slice(-50);
            });
          } catch (error) {
            console.error('Failed to parse event', error);
          }
        };

        socket.onerror = () => {
          if (!mounted) return;
          setState('error');
        };

        socket.onclose = () => {
          if (!mounted) return;
          setState('closed');
        };
      } catch (error) {
        console.error('WebSocket connection failed', error);
        setState('error');
      }
    };

    connect();

    return () => {
      mounted = false;
      wsRef.current?.close();
    };
  }, [active]);

  return { events, state };
}
