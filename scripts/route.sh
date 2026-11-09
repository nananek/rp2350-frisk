#!/usr/bin/env bash
# Placement -> DSN -> Freerouting -> SES -> GND pour.
#
# The board generator only creates the outline, footprints and nets; this
# script adds the copper.  Set FREEROUTING_CLASSPATH to the Freerouting 2.x
# CLI classpath (the jar plus its dependencies) before running.
set -euo pipefail
cd "$(dirname "$0")/.."

if [ -z "${FREEROUTING_CLASSPATH:-}" ]; then
  echo "Set FREEROUTING_CLASSPATH to the Freerouting CLI classpath." >&2
  echo "Example: export FREEROUTING_CLASSPATH=/opt/freerouting/freerouting.jar" >&2
  exit 1
fi

./scripts/kicad.sh python3 scripts/pcb_dsn.py
java -cp "$FREEROUTING_CLASSPATH" app.freerouting.cli.FreeroutingCli \
  -de pico2.dsn -do pico2.ses -mp 20
./scripts/kicad.sh python3 scripts/pcb_ses.py
./scripts/kicad.sh python3 scripts/finish_pcb.py
