#!/usr/bin/env bash
# Rebuild the JLCPCB fabrication outputs (gerbers, drill, BOM, CPL).
set -euo pipefail
cd "$(dirname "$0")/.."

PROJECT=pico2-compat
FAB=fab
rm -rf "$FAB"
mkdir -p "$FAB/gerbers" "$FAB/docs"

kicad-cli pcb export gerbers \
  --layers "F.Cu,In1.Cu,In2.Cu,B.Cu,F.Paste,B.Paste,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts" \
  --use-drill-file-origin \
  -o "$FAB/gerbers/" "$PROJECT.kicad_pcb"

kicad-cli pcb export drill --format excellon --excellon-units mm --excellon-separate-th \
  --drill-origin plot \
  -o "$FAB/gerbers/" "$PROJECT.kicad_pcb"

(cd "$FAB/gerbers" && python3 -c '
import glob, os, sys, zipfile
with zipfile.ZipFile(sys.argv[1], "w", zipfile.ZIP_DEFLATED) as z:
    for path in sorted(glob.glob("*")):
        if os.path.isfile(path):
            z.write(path, path)
' "../$PROJECT-gerbers.zip")

kicad-cli pcb export pos --format csv --units mm --side front --use-drill-file-origin \
  -o "$FAB/pos_kicad.csv" "$PROJECT.kicad_pcb"

python3 scripts/make_jlc_files.py

kicad-cli sch export pdf -o "$FAB/docs/schematic.pdf" "$PROJECT.kicad_sch"
kicad-cli pcb export pdf --layers "F.Cu,F.SilkS,Edge.Cuts" --mode-single \
  -o "$FAB/docs/pcb_top.pdf" "$PROJECT.kicad_pcb"
kicad-cli pcb export pdf --layers "B.Cu,B.SilkS,Edge.Cuts" --mirror --mode-single \
  -o "$FAB/docs/pcb_bottom.pdf" "$PROJECT.kicad_pcb"

ls -l "$FAB"
