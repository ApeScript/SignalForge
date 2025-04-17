<p align="center">

<img src="/assets/signalforge-header.png" alt="SignalForge" />

</p>

<p align="center">

<img src="https://img.shields.io/badge/python-3.11%2B-blue?style=flat-square" />
<img src="https://img.shields.io/badge/built%20with-FastAPI-0ba360?style=flat-square" />

</p>

<h1 align="center">SignalForge</h1>

<p align="center">
AI-Driven Crypto Signal Framework.<br>
100% Backend. Fully Dockerized. Ready for real usage.
</p>

---

# About SignalForge

SignalForge is a powerful AI-driven backend framework designed to analyze blockchain wallets, detect patterns, and generate trading signals.

Optimized for:
- Trading Bots
- On-Chain Analytics
- AI Signal Engines
- Crypto Infrastructure

This project runs exclusively via Docker for maximum stability, portability, and ease of use.

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.11 | Core Language  
| FastAPI | REST API Layer  
| SQLite | Local Database Storage  
| PyYAML | Config Management  
| OpenAI GPT | AI Analysis & Text Generation  
| Docker | Deployment & Environment  
| Uvicorn | API Server  
| Pytest | Testing  

---

## Folder Structure

```
/app/           → Python Package Root
/app/api/       → REST API with FastAPI
/app/cli/       → CLI commands & entry logic
/app/core/      → Main logic (data collection, analysis, signal generation)
/app/db/        → SQLite handling and models
/app/outputs/   → Exporters (JSON, Webhook, Report) & Logger
/app/config/    → Configurations & strategies (YAML based)
/app/tests/     → Pytest unit tests for all modules
/logs/          → Runtime logs
/signals/       → Generated signals
/reports/       → Generated reports
```

---

## Quick Start (Docker Only)

```bash
git clone https://github.com/ApeScript/SignalForge.git
cd SignalForge

cp .env.example .env

docker-compose up -d --build
```

---

## API Access

Once running:

> Swagger API UI:  
`http://localhost:8000/docs`

> Health Check:  
`http://localhost:8000/status`

---

## Available API Endpoints

| Method | Endpoint | Description |
|--------|-----------|-------------|
| GET | /status | API status check  
| POST | /scan | Wallet analysis  
| POST | /signal | Generate full signal  
| POST | /train | Add new pattern  

---

## Configuration

All configs live inside:

```
/app/config/
```

Strategy Files:
- `base_config.yaml`
- `strategy_aggressive.yaml`
- `strategy_conservative.yaml`

Customizable per project.

---

## Environment Variables

Configured via `.env`

Example:

```bash
OPENAI_API_KEY=sk-xxxxxxxx
RPC_URL=https://api.mainnet-beta.solana.com
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
TELEGRAM_CHAT_ID=-1001234567890
```

---

## Logs & Outputs

All logs and results are automatically stored in:

```
/logs/
/signals/
/reports/
```

Docker volumes ensure persistence.

---

## Testing

Run tests directly in the container:

```bash
docker-compose exec api pytest app/tests/
```

---

## Contribution

Open for Pull Requests.  
Keep it clean. Keep it smart.

---

## License

MIT License

---

## Links

- 🖥️ Website → [https://signalforge.codes/](https://signalforge.codes/)  
- 📚 Documentation → [https://synthara.gitbook.io/signalforge/](https://synthara.gitbook.io/signalforge/)  


<p align="center">
Built with ❤️ by <a href="https://github.com/ApeScript">ApeScript</a>
</p>
