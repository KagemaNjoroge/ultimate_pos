const { app, BrowserWindow } = require("electron");
const { spawn } = require("child_process");

let server;
const serverEndpoint = "http://localhost:8000";

function startServer() {
  server = spawn(
    "../.venv/Scripts/python.exe",
    ["../manage.py", "runserver", "8000"],
    {}
  );

  server.stdout.on("data", (data) => {
    console.log(`Server stdout: ${data}`);
  });

  server.stderr.on("data", (data) => {
    console.error(`Server stderr: ${data}`);
  });

  server.on("close", (code) => {
    console.log(`Server process exited with code ${code}`);
  });
}

function createWindow() {
  let win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
    },
  });
  win.loadURL(serverEndpoint);
}

app.on("ready", () => {
  startServer();
  createWindow();
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    if (server) {
      server.kill();
    }
    app.quit();
  }
});

app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    startServer();
    createWindow();
  }
});
