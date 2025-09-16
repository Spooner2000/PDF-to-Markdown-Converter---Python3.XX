import { create } from 'zustand';
import {
  fetchDashboardSummary,
  fetchDevices,
  fetchNotifications,
  fetchRoutines
} from '../services/api';

export type DashboardSummary = {
  counts: Record<string, number>;
  recent_logs: any[];
  recent_metrics: any[];
  notifications: any[];
  system_health: Record<string, string>;
};

type DashboardState = {
  summary?: DashboardSummary;
  routines: any[];
  devices: any[];
  notifications: any[];
  loading: boolean;
  error?: string;
  refresh: (token: string) => Promise<void>;
};

export const useDashboardStore = create<DashboardState>((set) => ({
  summary: undefined,
  routines: [],
  devices: [],
  notifications: [],
  loading: false,
  error: undefined,
  async refresh(token: string) {
    set({ loading: true, error: undefined });
    try {
      const [summary, routines, devices, notifications] = await Promise.all([
        fetchDashboardSummary(token),
        fetchRoutines(token),
        fetchDevices(token),
        fetchNotifications(token)
      ]);
      set({ summary: summary as DashboardSummary, routines, devices, notifications, loading: false });
    } catch (error) {
      console.error('Failed to load dashboard data', error);
      set({ error: 'Dashboarddaten konnten nicht geladen werden', loading: false });
    }
  }
}));
