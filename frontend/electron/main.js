const { app, BrowserWindow, ipcMain, nativeTheme } = require('electron');
const path = require('node:path');

const isDevelopment = !app.isPackaged;
const BACKEND_URL = process.env.BACKEND_URL ?? 'http://localhost:8000';

async function createWindow() {
  const window = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1200,
    minHeight: 720,
    backgroundColor: nativeTheme.shouldUseDarkColors ? '#1A1B1E' : '#FFFFFF',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    }
  });

  if (isDevelopment) {
    await window.loadURL('http://localhost:5173');
    window.webContents.openDevTools({ mode: 'detach' });
  } else {
    const indexPath = path.join(__dirname, '..', 'dist', 'index.html');
    await window.loadFile(indexPath);
  }
}

app.whenReady().then(() => {
  ipcMain.handle('backend-config', async () => ({ baseUrl: BACKEND_URL }));
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
