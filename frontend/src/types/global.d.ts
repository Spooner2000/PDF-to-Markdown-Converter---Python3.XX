declare global {
  interface Window {
    dashboardAPI?: {
      getBackendConfig: () => Promise<{ baseUrl: string }>;
    };
  }
}

export {};
