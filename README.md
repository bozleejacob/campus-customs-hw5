# Campus Customs — Multi-Agent Shop Ops

An agentic team (Boss, Inventory, Accounting, Facilities, Customer Service) that resolves tickets for a small campus shop, backed by an MCP server, a FastAPI backend, and a React dashboard.

See `AI_prompts.md` for the full build log. The final deliverables are in `output/` at the repo root.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd frontend
npm install
cd ..
```

Copy `.env.example` to `.env` and fill in your real `PORTKEY_API_KEY`. Never commit `.env`.

## Get a clean working database

Before any run (and any time you want to start fresh), copy the original database over the working copy:

```powershell
Copy-Item data\campus_customs.db data\campus_customs_new.db -Force
```

The app only ever reads/writes `data/campus_customs_new.db` — `data/campus_customs.db` is never modified. The backend's `POST /reset` route does the same copy for you once the backend is running (see below).

## 1. Start the MCP server

The MCP server (`mcp_server/server.py`) is what the agents use for every shop fact and the one allowed write (`record_payment`). It's launched automatically by the backend and by `.mcp.json` — you don't need to run it standalone, but you can smoke-test it directly:

```powershell
.\.venv\Scripts\python.exe mcp_server\server.py
```

## 2. Start the FastAPI backend

From `backend/`:

```powershell
cd backend
..\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000
```

This serves at `http://localhost:8000` and exposes: `GET /tickets`, `POST /tickets/{id}/run`, `GET /events`, `POST /payments/approve`, `GET /cash/balance`, `POST /reset`.

## 3. Start the React board

From `frontend/`:

```powershell
cd frontend
npm run dev
```

This serves the dashboard at `http://localhost:5173`. It talks to the backend at `http://localhost:8000` (CORS is already configured for this origin).

## Before a full three-ticket run

Reset the database first, either via the dashboard's "Reset Shop" button or:

```powershell
curl.exe -X POST http://localhost:8000/reset
```

Then run tickets 101, 102, and 103 from the dashboard (or `POST /tickets/{id}/run`), approving any recommended payments through the dashboard's Approve Payment modal (or `POST /payments/approve`). Every tool call, delegation, and final output is appended to `output/audit_trail.json` — it's never wiped, so history accumulates across runs.

## Repo layout

- `mcp_server/` — the FastMCP server and its tools
- `backend/` — the FastAPI app, the five PydanticAI agents, and their prompts
- `frontend/` — the React + Vite + TypeScript dashboard
- `data/` — the original database and the working copy
- `output/` — final deliverables (harness, smoke test, desk tickets, design notes, resolved tickets, resolved board, audit trail)
