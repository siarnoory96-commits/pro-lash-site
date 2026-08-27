# Hermes Orchestration — Pro Lash

## Runner
- **Language/runtime:** Python 3 (already on this machine; no Node/npm installed, so the runner is Python-based rather than Node-based).
- **Trigger engine:** none live yet. Designed for internal cron-style timers once there's something worth polling — see "Honest status" below.
- **How an agent is invoked:** the SOP's default pattern (`spawn('claude', ['-p'], ...)` via the existing Claude Code login, no API key) requires the `claude` CLI on `PATH`. It isn't — confirmed via `type claude` → not found. So today, the orchestrator's allowlist/routing logic is real and runnable, but it cannot programmatically re-invoke a fresh agent response in this environment. It replays and classifies **real, already-generated agent outputs** (from `agents/test-log.md`) through the actual guardrail logic — proving the fence works, even though the "generate a new reply" half of the loop needs either the `claude` CLI installed and on `PATH`, or a direct Anthropic API key.

## Per-agent schedule/trigger (designed, not yet live)
- **`pro-lash-engagement`:** would trigger on new Instagram/TikTok DM or comment (event-driven). No trigger exists — Instagram/TikTok DM access requires Meta/TikTok Business API approval, which is a platform-level gate neither of us can self-serve (see `agents/README.md`).
- **`pro-lash-content`:** would trigger on a schedule (e.g. daily) to refresh the content pipeline. No scheduler is deployed yet — see honest status below.

## Flow of one run
```
trigger → load scoped key → check allowlist →
  if action ∈ autonomous list → execute + append audit + push to dashboard
  if action ∉ autonomous list (irreversible / money / risk / edge case) → DON'T execute → escalate + append audit
```
This flow is implemented for real in `ops/orchestrator/run.py` and verified in Step 7 (see `ops/audit.log`) — using the real Lesson 6 test tasks as input, since there's no live trigger to pull from yet.

## Health
- **Heartbeat:** each run writes a timestamped line to `ops/audit.log`. No always-on process exists yet to heartbeat continuously — see honest status.
- **Restart:** would be `restart: unless-stopped` in `ops/docker-compose.yml` (written, not yet build-tested — Docker isn't installed on this machine).
- **Kill switch:** `ops/orchestrator/run.py --halt` sets `ops/HALT` — checked at the top of every run; if present, the runner refuses to execute anything and logs the refusal. Tested in Step 7.

## Honest status — what's real vs. designed
| Piece | Status |
|---|---|
| Allowlist enforcement logic | **Real, runnable, tested** (`ops/orchestrator/run.py`) |
| Audit log | **Real** — seeded from actual Lesson 6 test runs + this lesson's verification run |
| Kill switch | **Real, tested** |
| Containerization (Docker) | **Written, not build-tested** — Docker isn't installed |
| Scheduling / live triggers | **Designed, not deployed** — no live event source exists (no Instagram/TikTok API access; Shopify has a store but no Admin API token wired in yet) |
| "Runs 24/7" | **Not true yet, and not claimed.** Nothing is currently running unattended. This spec and the tested runner are the infrastructure ready to deploy once a real trigger and a host exist. |
