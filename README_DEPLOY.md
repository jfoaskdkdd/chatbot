Deployment notes — minimal steps to run this bot on a VPS or via Docker

1) Recommended: run inside a Docker container
- The bot depends on a Chrome/Chromium binary. The included Dockerfile installs common system libs but expects either Chrome to be installed in the image or the host to mount a Chrome binary and set `PUPPETEER_EXECUTABLE_PATH`.

2) Quick Docker run (example)
- Build image:
  docker build -t whatsapp-bot .
- Run (mount tokens and data):
  docker run -d --name whatsapp-bot \
    -v "$(pwd)/tokens:/usr/src/app/tokens" \
    -v "$(pwd)/contatos_filtrados.json:/usr/src/app/contatos_filtrados.json:ro" \
    -v "$(pwd)/audio_resposta.ogg:/usr/src/app/audio_resposta.ogg:ro" \
    -e PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome-stable \
    whatsapp-bot

3) Non-Docker VPS setup
- Install Node.js (recommended v18+ or Node 20 LTS). Install Chrome/Chromium on the server.
- Copy repo to server and run:
  npm ci --production
  export PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome-stable
  export PUPPETEER_DUMPIO=1 (optional for debugging)
  node chatbot.js

4) Cleaning workspace
- Use `prune_workspace.ps1` on Windows to list candidate files that are unlikely to be used on the VPS (CSV task files, local scripts). Run with `-Run` to actually move them to a `pruned_files_YYYYMMDD_HHMMSS` folder.

5) Git ignore
- `.gitignore` is included and excludes `tokens/`, logs, caches and local state files.

6) Environment
- Copy `.env.example` to `.env` and adjust variables. Avoid committing `.env`.

7) Security
- Keep `tokens/` private. Don't commit them.
- If using Docker, mount the `tokens/` dir from the host to persist session data.

Questions?
- If you want I can:
  - Make a systemd unit file for running the bot as a service on the VPS.
  - Produce a smaller Docker image with Chrome included (larger image) or use a multi-stage build.
  - Make a health-check endpoint or a small express wrapper to monitor the bot.
