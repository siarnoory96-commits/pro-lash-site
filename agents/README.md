# Pro Lash Agents

Two voice-trained agents, both draft-only (no Instagram/TikTok/scheduler MCP connected yet — nothing here can post, send, or act on its own).

## `pro-lash-engagement`
Drafts replies to Instagram/TikTok DMs and comments. Handles the 5 known objections (irritation fear, extension-safety, "is organic weaker," price, "tried serums before") plus friendly comments and honest pre-launch answers. **Escalates:** adverse-reaction reports, press/collab inquiries, anything about money/orders (no store exists), any fact not in the foundation files.

**Run it:** paste a real DM/comment and ask Claude to use the `pro-lash-engagement` subagent — or just say "draft a reply to this" in a Pro Lash session.

## `pro-lash-content`
Drafts on-brand captions, content hooks, and posting calendars — every idea traceable to one of the 6 necessary beliefs. **Escalates:** invented stats/percentages, fake testimonials (hard refuse, always), named-competitor comparisons without sign-off.

**Run it:** ask for a caption, a batch of hooks, or a calendar in a Pro Lash session.

## Test results
6/6 on both agents, first pass — see `test-log.md` for every task, output, and escalation call. No tuning needed yet; re-run this test suite (plus any new edge cases you hit in the wild) before loosening any allowlist.

## How to change the fence
Edit `<agent>/spec.md`'s Allowlist / Human-in-the-loop / Escalate sections, then mirror the change into the matching `~/.claude/agents/pro-lash-*.md` subagent file (that's the file that actually runs). **Widen what an agent can do only after a new round of tests passes** — more power always means more hardening, not less.

## How to revoke access
Delete or rename the subagent file at `~/.claude/agents/pro-lash-engagement.md` or `~/.claude/agents/pro-lash-content.md` — since nothing is connected to a live tool, that fully disables the agent immediately.

## What happens when you actually connect Instagram/TikTok
Right now both agents draft; a human sends. Once real MCP/API access exists, the spec's Allowlist section defines what could move to auto-send — but per the SOP's access paradox, more autonomy means the guardrails get *tighter* first, not looser. Don't flip that switch without a fresh test round on the live connection.
