const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('dashboardAPI', {
  async getBackendConfig() {
    return ipcRenderer.invoke('backend-config');
  }
});
