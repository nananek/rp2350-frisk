"""Add the copper pours/planes and fill them.

Four-layer stack:
  F.Cu  : signals + local 1V1 pour around the RP2350 + GND pour
  In1   : GND plane
  In2   : 3V3 plane
  B.Cu  : signals + GND pour
"""

import os
import sys

import pcbnew

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 57.6, 31.4
CHAMFER = 2.0

import re


def strip_zones_text(src, dst):
    """Remove top-level zone s-expressions without pcbnew.

    Removing zones through the Python API and saving immediately afterwards
    leaves a board that the KiCad 10 Python loader cannot wrap correctly, so
    this small text pass is used instead.
    """
    text = open(src, encoding="utf-8").read()
    out, last = [], 0
    for m in re.finditer(r"(?m)^[ \t]*\(zone\b", text):
        out.append(text[last:m.start()])
        i = m.start() + m.group(0).rfind("(")
        depth = 0
        in_string = False
        escaped = False
        while i < len(text):
            c = text[i]
            if in_string:
                if escaped:
                    escaped = False
                elif c == "\\":
                    escaped = True
                elif c == '"':
                    in_string = False
            else:
                if c == '"':
                    in_string = True
                elif c == "(":
                    depth += 1
                elif c == ")":
                    depth -= 1
                    if depth == 0:
                        i += 1
                        break
            i += 1
        last = i
    out.append(text[last:])
    open(dst, "w", encoding="utf-8").write("".join(out))


SRC = os.path.join(ROOT, "pico2-compat.kicad_pcb")
TMP = os.path.join(ROOT, ".tmp_no_zones.kicad_pcb")
strip_zones_text(SRC, TMP)
b = pcbnew.LoadBoard(TMP)
os.remove(TMP)

gnd = b.FindNet("GND")
v11 = b.FindNet("1V1")
v33 = b.FindNet("3V3")
if not all((gnd, v11, v33)):
    raise SystemExit("power nets not found")

# 0.3 mm inset, corners cut a little deeper than the board chamfer.
m, leg = 0.3, CHAMFER + 1.0
board_outline = [
    (m, H / 2.0), (m, H - m - leg), (m + leg, H - m),
    (W - m - leg, H - m), (W - m, H - m - leg), (W - m, m + leg),
    (W - m - leg, m), (m + leg, m), (m, m + leg),
]


def add_zone(net, layer, outline, priority=0):
    z = pcbnew.ZONE(b)
    ls = pcbnew.LSET()
    ls.AddLayer(layer)
    z.SetLayerSet(ls)
    z.SetNet(net)
    o = z.Outline()
    o.NewOutline()
    for x, y in outline:
        o.Append(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
    z.SetLocalClearance(pcbnew.FromMM(0.2))
    z.SetMinThickness(pcbnew.FromMM(0.2))
    z.SetThermalReliefGap(pcbnew.FromMM(0.25))
    z.SetThermalReliefSpokeWidth(pcbnew.FromMM(0.3))
    z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
    z.SetAssignedPriority(priority)
    b.Add(z)
    return z


add_zone(gnd, pcbnew.F_Cu, board_outline)
add_zone(gnd, pcbnew.B_Cu, board_outline)
add_zone(gnd, pcbnew.In1_Cu, board_outline)
add_zone(v33, pcbnew.In2_Cu, board_outline)

for d in b.GetDrawings():
    if d.GetLayer() == pcbnew.B_SilkS and hasattr(d, "SetMirrored"):
        d.SetMirrored(True)

pcbnew.ZONE_FILLER(b).Fill(b.Zones())
pcbnew.SaveBoard(os.path.join(ROOT, "pico2-compat.kicad_pcb"), b)
print("filled zones:", len(list(b.Zones())))
