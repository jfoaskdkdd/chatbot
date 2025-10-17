README: Running the WhatsApp bot on a VPS (non-Docker)

This file explains minimal steps to run the bot on a Linux VPS (Debian/Ubuntu).

Prerequisites
- A Linux VPS (Debian/Ubuntu recommended).
- Node.js (v18+ or v20 LTS recommended).
- Chrome or Chromium installed (the bot needs a browser binary for puppeteer/wppconnect).

Quick setup
1. Copy repository to the VPS (git clone or rsync).
2. Install Node and Chrome:
   sudo apt update
   sudo apt install -y curl ca-certificates
   # Node 20 example
   curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
   sudo apt install -y nodejs
   # Chrome (recommended)
   wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
   sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list'
   sudo apt update
   sudo apt install -y google-chrome-stable

3. Install npm dependencies and prepare env:
   cd /path/to/chatbot
   npm ci --production
   cp .env.example .env
   # edit .env as needed (PUPPETEER_EXECUTABLE_PATH, MAX_OPA, etc.)

4. Run the bot in foreground (for testing):
   export PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome-stable
   export PUPPETEER_DUMPIO=1   # optional for Chromium stderr
   node chatbot.js

Systemd service example (production)
- Create `/etc/systemd/system/chatbot.service` with the following content (edit paths):

  [Unit]
  Description=WhatsApp Chatbot (wppconnect)
  After=network.target

  [Service]
  Type=simple
  WorkingDirectory=/path/to/chatbot
  ExecStart=/usr/bin/node /path/to/chatbot/chatbot.js
  Restart=on-failure
  Environment=NODE_ENV=production
  Environment=PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome-stable
  Environment=PUPPETEER_DUMPIO=0

  [Install]
  WantedBy=multi-user.target

- Then enable and start:
  sudo systemctl daemon-reload
  sudo systemctl enable chatbot
  sudo systemctl start chatbot

Cleaning workspace before commit
- `.gitignore` added to this repo excludes tokens/, logs and caches.
- Use `prune_workspace.ps1` on Windows if you want to move CSVs and helper scripts out of the repo before pushing.

Notes
- Docker removed from the repo per your request. Files deleted: Dockerfile, docker-compose.yml, .dockerignore.
- If you later decide you want a container, I can reintroduce a minimal Dockerfile that includes Chrome.

Need me to create the `chatbot.service` file in the repo (for your review) so you can SCP it to `/etc/systemd/system/`? Reply yes/no and I will add it.