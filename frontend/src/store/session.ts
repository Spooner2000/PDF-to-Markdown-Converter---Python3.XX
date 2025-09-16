import { create } from 'zustand';
import { loginRequest } from '../services/api';

type UserProfile = {
  username: string;
  full_name: string;
  roles: string[];
};

type SessionState = {
  token?: string;
  user?: UserProfile;
  expiresAt?: string;
  loading: boolean;
  error?: string;
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => void;
};

export const useSessionStore = create<SessionState>((set) => ({
  token: undefined,
  user: undefined,
  expiresAt: undefined,
  loading: false,
  error: undefined,
  async login(username: string, password: string) {
    set({ loading: true, error: undefined });
    try {
      const response = await loginRequest(username, password);
      set({
        token: response.token,
        user: response.user,
        expiresAt: response.expires_at,
        loading: false,
      });
      return true;
    } catch (error) {
      console.error('Login failed', error);
      set({ error: 'Anmeldung fehlgeschlagen', loading: false });
      return false;
    }
  },
  logout() {
    set({ token: undefined, user: undefined, expiresAt: undefined, error: undefined });
  }
}));
