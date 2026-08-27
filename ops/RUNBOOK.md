# Hermes Runbook — Pro Lash

## Current real status (read this first)
**Nothing is running unattended right now.** This is tested, working orchestration *logic* — not a live 24/7 deployment. Here's the honest breakdown:

| Component | Status |
|---|---|
| Allowlist enforcement (`ops/orchestrator/run.py`) | ✅ Real, tested — 12/12 real Lesson 6 tasks routed correctly, off-allowlist actions correctly refused, kill switch tested live |
| Audit log (`ops/audit.log`) | ✅ Real, append-only, contains the actual verification run |
| Containerization (`Dockerfile`, `docker-compose.yml`) | ⚠️ Written, not build-tested — Docker isn't installed on this machine |
| Live triggers / scheduling | ❌ Not deployed — no connected event source exists yet |
| Escalation channel | ❌ Not connected — no Slack/email wired in; escalations only exist in the audit log today |

**What's blocking full deployment:** (1) Docker on a host, (2) a real live trigger — Instagram/TikTok needs Business API approval (not self-serve), Shopify needs the Admin API token we shelved, (3) somewhere for escalations to actually reach a human (Slack, email, or just "check the log").

## Start (once Docker is installed and a host is chosen)
```bash
cd ops/
cp .env.example .env        # fill in real values as they're provisioned
docker compose up -d
docker compose ps           # confirm "Up"
docker compose logs -f      # watch it run
```

## Stop
```bash
docker compose down
```

## Inspect
```bash
docker compose logs -f hermes         # live logs
tail -f ops/audit.log                 # the audit trail, human-readable (one JSON line per action)
cat ops/HALT 2>/dev/null && echo "HALTED" || echo "running normally"
```

## Restart (confirm it comes back)
```bash
docker compose restart
docker compose ps    # confirm "Up" again
```

## Rotate a key
1. Generate the new key at the source (e.g. Shopify Admin API, Instagram Business).
2. Update the value in `ops/.env` (never in the Dockerfile or compose file).
3. `docker compose up -d` — reloads the container with the new env value.
4. Old key still works until you revoke it at the source — revoke it there once the new one's confirmed working.

## Kill switch — halt ALL agents immediately
```bash
python3 ops/orchestrator/run.py --halt
```
Every subsequent run refuses to execute anything (verified in Lesson 8's test — a normally-autonomous action was correctly refused while halted). To resume:
```bash
python3 ops/orchestrator/run.py --resume
```

## Where exceptions land
**Today: nowhere automatic.** They're appended to `ops/audit.log` with `"decision": "human_in_the_loop"` or `"decision": "escalate"` — a human has to check the log. Once `ESCALATION_CHANNEL_WEBHOOK` in `.env` is set to a real Slack/email endpoint, wire it into `run_task()` in `orchestrator/run.py` so escalations push instead of waiting to be found.

## Widening what an agent can do
Edit `ops/allowlist.yml` — move an action from `human_in_the_loop` to `autonomous` only after a fresh round of tests passes against the *live* tool (not just the replayed Lesson 6 tasks). More power always means more hardening first, never less.
