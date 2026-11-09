#!/usr/bin/env bash
# Regenerate docs/pcb_top.png, pcb_bottom.png and pcb_routing.png.
set -euo pipefail
cd "$(dirname "$0")/.."

PROJECT=pico2-compat
WIDTH=1800
DPI=$(python3 -c "print(f'{$WIDTH * 25.4 / 57.6:.4f}')")

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

sed 's/(paper "A4")/(paper "User" 57.6 31.4)/' "$PROJECT.kicad_pcb" > "$TMP/board.kicad_pcb"
python3 scripts/strip_zones.py "$TMP/board.kicad_pcb" "$TMP/board_routing.kicad_pcb"

plot() {
  local layers=$1 name=$2 board=$3
  shift 3
  kicad-cli pcb export pdf --layers "$layers" -o "$TMP/$name.pdf" "$@" "$board" >/dev/null
  gs -q -dNOPAUSE -dBATCH -sDEVICE=png16m -r"$DPI" \
    -o "docs/$name.png" "$TMP/$name.pdf"
  echo "wrote docs/$name.png"
}

plot "F.Cu,F.SilkS,Edge.Cuts" pcb_top "$TMP/board.kicad_pcb"
plot "B.Cu,B.SilkS,Edge.Cuts" pcb_bottom "$TMP/board.kicad_pcb" --mirror
plot "F.Cu,In1.Cu,In2.Cu,B.Cu,F.SilkS,Edge.Cuts" pcb_routing "$TMP/board_routing.kicad_pcb"
kicad-cli sch export pdf -o docs/schematic.pdf "$PROJECT.kicad_sch" >/dev/null
echo "wrote docs/schematic.pdf"
