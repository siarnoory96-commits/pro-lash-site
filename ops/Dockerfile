# Hermes orchestrator — Pro Lash
#
# HONEST STATUS: written but NOT build-tested. Docker isn't installed on the
# machine this was built on (`docker --version` → command not found). This is
# the containment design per the Hermes SOP, ready to build once Docker exists
# on a host — don't treat "the Dockerfile exists" as "the layer is containerized."

FROM python:3.11-slim

WORKDIR /app

COPY orchestrator/ /app/orchestrator/
COPY allowlist.yml /app/allowlist.yml

# No external Python deps required today — run.py's YAML reader is hand-rolled
# specifically to avoid needing pip installs inside the image. If a real agent
# invocation path (e.g. the `claude` CLI) is added later, install it here.

# Runs as a non-root user — least privilege inside the container too.
RUN useradd -m hermes
USER hermes

# Placeholder long-running command — the SOP's design is cron-style timers or
# an event/queue listener inside this process. Today there's no live trigger to
# listen for (see orchestration-spec.md), so this just keeps the container up
# for `docker compose exec` verification runs until a real trigger exists.
CMD ["python3", "-u", "orchestrator/run.py"]
