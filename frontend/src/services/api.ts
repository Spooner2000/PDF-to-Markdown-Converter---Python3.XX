import axios, { AxiosRequestConfig } from 'axios';

type BackendConfig = {
  baseUrl: string;
};

const DEFAULT_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';
let cachedBackendUrl: string | null = null;

export async function getBackendBaseUrl(): Promise<string> {
  if (cachedBackendUrl) {
    return cachedBackendUrl;
  }
  if (window.dashboardAPI?.getBackendConfig) {
    try {
      const cfg = await window.dashboardAPI.getBackendConfig();
      cachedBackendUrl = cfg?.baseUrl ?? DEFAULT_BASE_URL;
      return cachedBackendUrl;
    } catch (error) {
      console.warn('Falling back to default backend URL', error);
    }
  }
  cachedBackendUrl = DEFAULT_BASE_URL;
  return cachedBackendUrl;
}

export async function apiRequest<T>(config: AxiosRequestConfig, token?: string): Promise<T> {
  const baseUrl = await getBackendBaseUrl();
  const response = await axios.request<T>({
    baseURL: `${baseUrl.replace(/\/$/, '')}/api/v1`,
    ...config,
    headers: {
      ...(config.headers ?? {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {})
    }
  });
  return response.data;
}

export async function loginRequest(username: string, password: string) {
  return apiRequest<{ token: string; expires_at: string; user: { username: string; full_name: string; roles: string[] } }>({
    url: '/auth/login',
    method: 'POST',
    data: { username, password }
  });
}

export async function fetchDashboardSummary(token: string) {
  return apiRequest<Record<string, unknown>>({
    url: '/dashboard/summary',
    method: 'GET'
  }, token);
}

export async function fetchRoutines(token: string) {
  return apiRequest<any[]>({
    url: '/routines',
    method: 'GET'
  }, token);
}

export async function fetchDevices(token: string) {
  return apiRequest<any[]>({
    url: '/devices',
    method: 'GET'
  }, token);
}

export async function fetchNotifications(token: string) {
  return apiRequest<any[]>({
    url: '/observability/notifications',
    method: 'GET'
  }, token);
}
