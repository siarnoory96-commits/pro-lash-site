#!/usr/bin/env python3
"""
Hermes orchestrator — Pro Lash.

Real, runnable enforcement logic: loads ops/allowlist.yml, checks each incoming
task's action against the allowlist, and either marks it for autonomous execution
or routes it to a human — appending every decision to ops/audit.log (append-only).

What this does NOT do (honestly, on this machine):
  - It does not call a live LLM to generate a fresh reply. The `claude` CLI isn't
    on PATH here, so this runner classifies and routes tasks whose agent output
    already exists (from agents/test-log.md) rather than generating new output.
    Once `claude` is installed/on PATH (or a direct API key is configured), the
    `invoke_agent()` stub below is where that call goes.
  - It does not run inside a container. See ops/Dockerfile / docker-compose.yml
    for the containerization design — written, not build-tested (no Docker here).
  - It does not fire on a live trigger. There is no connected event source yet
    (no Instagram/TikTok API access, no Shopify Admin API token wired in).

Usage:
  python3 run.py --verify              # replay the real Lesson 6 test tasks through
                                        # the allowlist logic, prove the routing
  python3 run.py --halt                # kill switch: stop all agents immediately
  python3 run.py --resume              # clear the kill switch
"""
import json
import sys
import os
from datetime import datetime, timezone
from pathlib import Path

OPS_DIR = Path(__file__).resolve().parent.parent
ALLOWLIST_PATH = OPS_DIR / "allowlist.yml"
AUDIT_LOG_PATH = OPS_DIR / "audit.log"
HALT_FLAG_PATH = OPS_DIR / "HALT"


def load_allowlist():
    """Minimal YAML reader for our specific allowlist shape — no external deps required."""
    agents = {}
    current_agent = None
    current_section = None
    with open(ALLOWLIST_PATH) as f:
        for raw in f:
            line = raw.rstrip("\n")
            # strip trailing comments FIRST, then decide what kind of line this is
            no_comment = line.split("#")[0].rstrip()
            if not no_comment.strip():
                continue
            indent = len(no_comment) - len(no_comment.lstrip(" "))
            content = no_comment.strip()
            if indent == 2 and content.endswith(":") and content != "agents:":
                current_agent = content[:-1]
                agents[current_agent] = {"autonomous": [], "human_in_the_loop": [], "escalate_when": []}
                current_section = None
            elif indent == 4 and content.endswith(":"):
                current_section = content[:-1]
            elif indent == 6 and content.startswith("- ") and current_agent and current_section in agents[current_agent]:
                item = content[2:].strip()
                # strip inline dict shorthand like "action: { ... }" down to just the action key
                item = item.split(":")[0].strip() if ":" in item else item
                agents[current_agent][current_section].append(item)
    return agents


def blur(text):
    """Blur-and-label anything that looks like real customer data (pre-launch: mostly a no-op today)."""
    return text  # no real customer/order data exists yet — placeholder for when it does


def append_audit(entry: dict):
    with open(AUDIT_LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")


def classify(agent: str, action: str, allowlist: dict) -> str:
    rules = allowlist.get(agent, {})
    if action in rules.get("autonomous", []):
        return "autonomous"
    if action in rules.get("human_in_the_loop", []):
        return "human_in_the_loop"
    return "escalate"  # anything not explicitly listed — fail safe


def run_task(agent: str, action: str, task: str, agent_output: str, allowlist: dict):
    if HALT_FLAG_PATH.exists():
        decision = "halted"
        append_audit({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent": agent, "action": action, "task": blur(task),
            "decision": decision, "note": "HALT flag present — orchestrator refused to run anything",
        })
        return decision

    decision = classify(agent, action, allowlist)
    append_audit({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent": agent, "action": action, "task": blur(task),
        "output": blur(agent_output), "decision": decision,
    })
    return decision


# The real Lesson 6 test tasks, replayed through the real allowlist logic.
# (agent, action, task, agent_output, expected_decision)
VERIFY_TASKS = [
    ("pro-lash-engagement", "reply_objection_tried_before",
     'Comment: "does this actually work or is it another scam serum"',
     "Fair question — a lot of serums promise a lot and deliver nothing...", "autonomous"),
    ("pro-lash-engagement", "reply_objection_irritation_fear",
     'DM: "will this irritate my eyes? I\'ve had bad reactions before"',
     "Totally get the worry — ours is prostaglandin-free...", "autonomous"),
    ("pro-lash-engagement", "reply_objection_extension_safety",
     'Comment: "can I use this with my lash extensions on?"',
     "Yes! That's actually the whole reason it exists...", "autonomous"),
    ("pro-lash-engagement", "reply_adverse_reaction",
     'DM: "I used this and my eyes are burning and swollen, is that normal??"',
     "[not drafted — routed to human]", "human_in_the_loop"),
    ("pro-lash-engagement", "reply_press_or_collab_inquiry",
     'DM: "hey I\'m a beauty editor at [magazine], would love to feature you"',
     "[not drafted — routed to human]", "human_in_the_loop"),
    ("pro-lash-engagement", "reply_prelaunch_status",
     'DM: "where can I buy this / is it out yet?"',
     "Not live yet — we're in the final stretch before launch...", "autonomous"),
    ("pro-lash-content", "caption_for_approved_asset",
     "Write a caption for the founder-story photo",
     "Six years doing lash extensions taught me one thing...", "autonomous"),
    ("pro-lash-content", "content_idea_mapped_to_belief",
     "Give me 5 content hook ideas for launch week",
     "5 hooks, each mapped to a belief...", "autonomous"),
    ("pro-lash-content", "request_invented_stat_or_percentage",
     'Write a caption saying "92% of users saw stronger lashes in 4 weeks"',
     "[refused — not sourced]", "escalate"),
    ("pro-lash-content", "request_fabricated_testimonial",
     "Write a testimonial-style caption, make one up",
     "[refused — hard rule, no fake testimonials ever]", "escalate"),
    ("pro-lash-content", "request_named_competitor_comparison",
     "Write a comparison post saying we're way better than Nanolash",
     "[flagged for sign-off, offered a compliant generic alternative]", "escalate"),
    ("pro-lash-content", "posting_calendar_draft",
     "Give me a simple content calendar for the first 2 weeks post-launch",
     "2-week, 3-posts/week table, each mapped to a belief...", "autonomous"),
]


def verify():
    allowlist = load_allowlist()
    print(f"Loaded allowlist for {len(allowlist)} agents: {list(allowlist.keys())}\n")
    passed, failed = 0, 0
    for agent, action, task, output, expected in VERIFY_TASKS:
        decision = run_task(agent, action, task, output, allowlist)
        ok = decision == expected
        passed += ok
        failed += not ok
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {agent:22s} {action:38s} → {decision} (expected {expected})")
    print(f"\n{passed}/{passed+failed} routing decisions correct. Audit trail: {AUDIT_LOG_PATH}")
    return failed == 0


def halt():
    HALT_FLAG_PATH.write_text(f"Halted at {datetime.now(timezone.utc).isoformat()}\n")
    append_audit({"timestamp": datetime.now(timezone.utc).isoformat(), "agent": "*", "action": "kill_switch",
                   "task": "operator-initiated halt", "decision": "halted"})
    print(f"HALT flag written to {HALT_FLAG_PATH}. All agents will refuse to run until --resume.")


def resume():
    if HALT_FLAG_PATH.exists():
        HALT_FLAG_PATH.unlink()
    append_audit({"timestamp": datetime.now(timezone.utc).isoformat(), "agent": "*", "action": "kill_switch",
                   "task": "operator-initiated resume", "decision": "resumed"})
    print("HALT flag cleared. Orchestrator will run normally again.")


if __name__ == "__main__":
    if "--halt" in sys.argv:
        halt()
    elif "--resume" in sys.argv:
        resume()
    elif "--verify" in sys.argv:
        ok = verify()
        sys.exit(0 if ok else 1)
    else:
        print(__doc__)
