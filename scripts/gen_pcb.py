"""Generate pico2-compat.kicad_pcb with pcbnew (KiCad 10).

The board outline is the same 57.6 x 31.4 mm, 2 mm 45-degree corner cut
outline as nananek/serial-km-emulator.  The Pico-compatible 2x20 header
uses the real Pico pin order (pin 1 at the USB end, 2.54 mm pitch,
17.78 mm row spacing).  The three Type-C ports are on the right short edge
(native USB) and the bottom long edge (PIO USB and CH343P UART).

Run this script with the KiCad Python module, then route with Freerouting
(see scripts/route.sh) and run the DRC.
"""

import math
import os
import sys

import pcbnew

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from design import PROJECT, PARTS, GND, VSYS, P3V3, P1V1  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FP_DIR = os.path.join(ROOT, "lib", "PICO2.pretty")

W, H = 57.6, 31.4
CHAMFER = 2.0
THICKNESS = 1.6

# ref -> (x, y, rotation)
PLACE = {
    "U1": (35.0, 11.0, 0),
    "U2": (44.5, 7.5, 0),
    "U3": (29.0, 23.6, 0),
    "U4": (22.0, 23.2, 0),
    "J1": (55.2, 10.5, 90),
    "J2": (13.5, 29.0, 0),
    "J3": (44.5, 29.0, 0),
    "J4": (27.5, 28.5, 90),
    "J5A": (1.37, 2.2, 0),
    "J5B": (1.37, 19.98, 0),
    "Y1": (27.5, 13.0, 0),
    "SW1": (4.0, 24.2, 0),
    "SW2": (53.8, 24.3, 0),
    "D1": (49.0, 16.5, 180),
    "D2": (14.0, 22.0, 180),
    "D3": (38.0, 22.0, 180),
    "D4": (49.0, 6.0, 180),
    "D5": (8.0, 22.0, 180),
    "D6": (48.0, 22.0, 180),
    "R1": (48.0, 22.0, 0),
    "R2": (51.0, 22.0, 0),
    "R3": (10.6, 22.6, 0),
    "R4": (14.2, 22.6, 0),
    "R5": (40.5, 22.0, 0),
    "R6": (43.0, 22.0, 0),
    "R7": (46.0, 11.5, 0),
    "R8": (46.0, 13.5, 0),
    "R9": (10.5, 17.5, 0),
    "R10": (13.0, 17.5, 0),
    "R11": (8.0, 17.5, 0),
    "R12": (17.5, 21.0, 0),
    "R13": (49.0, 21.0, 0),
    "R14": (40.0, 6.0, 0),
    "R15": (30.0, 7.0, 0),
    "R16": (30.0, 14.0, 0),
    "R17": (22.0, 21.0, 0),
    "R18": (24.0, 21.0, 0),
    "R19": (26.0, 21.0, 0),
    "R20": (29.0, 16.5, 0),
    "L1": (40.4, 14.0, 0),
    "C1": (55.5, 17.5, 0),
    "C2": (15.8, 21.0, 0),
    "C3": (36.6, 22.6, 0),
    "C4": (50.5, 4.0, 0),
    "C5": (18.5, 21.8, 0),
    "C6": (36.0, 26.0, 0),
    "C7": (18.0, 23.5, 0),
    "C8": (20.0, 23.5, 0),
    "C9": (24.6, 22.6, 0),
    "C10": (25.0, 23.5, 0),
    "C11": (40.4, 8.0, 0),
    "C12": (40.4, 9.5, 0),
    "C13": (33.0, 4.5, 0),
    "C14": (35.0, 4.5, 0),
    "C15": (37.0, 4.5, 0),
    "C16": (29.0, 9.0, 0),
    "C17": (40.4, 11.0, 0),
    "C18": (40.4, 12.5, 0),
    "C19": (40.4, 15.5, 0),
    "C20": (39.0, 4.5, 0),
    "C21": (31.0, 4.5, 0),
    "C22": (33.5, 21.0, 0),
    "C23": (35.0, 21.0, 0),
    "C24": (37.5, 16.0, 0),
    "C25": (31.5, 17.5, 0),
    "C26": (36.5, 17.5, 0),
    "C27": (33.5, 23.0, 0),
    "C28": (22.0, 22.0, 0),
    "C29": (29.0, 15.0, 0),
    "LED1": (24.0, 22.5, 180),
    "LED2": (26.0, 22.5, 180),
}# Pin labels for the Pico header: pin number -> short label.
HEADER_LABELS = {
    1: "GP0", 2: "GP1", 3: "GND", 4: "GP2", 5: "GP3", 6: "GP4", 7: "GP5",
    8: "GND", 9: "GP6", 10: "GP7", 11: "GP8", 12: "GP9", 13: "GND",
    14: "GP10", 15: "GP11", 16: "GP12", 17: "GP13", 18: "GND", 19: "GP14",
    20: "GP15", 21: "GP16", 22: "GP17", 23: "GND", 24: "GP18", 25: "GP19",
    26: "GP20", 27: "GP21", 28: "GND", 29: "GP22", 30: "RUN", 31: "GP26",
    32: "GP27", 33: "GND", 34: "GP28", 35: "VREF", 36: "3V3", 37: "3V3EN",
    38: "GND", 39: "VSYS", 40: "VBUS",
}

# Large parts are placed by hand.  Every other part is packed by a small
# rectangle allocator so that courtyards and solder-mask openings do not
# collide on this crowded 57.6 x 31.4 mm board.
FIXED = {"U1", "U2", "U3", "U4", "J1", "J2", "J3", "J4", "J5A", "J5B", "Y1", "SW1", "SW2"}

# Conservative keep-out boxes for the fixed parts (board mm).
FIXED_BOX = {
    "J5A": (0.3, 0.8, 50.6, 3.6),
    "J5B": (0.3, 18.6, 50.6, 21.45),
    "J1": (49.2, 5.0, 57.6, 15.8),
    "J2": (8.0, 23.6, 19.0, 31.4),
    "J3": (38.8, 23.6, 50.0, 31.4),
    "SW1": (0.5, 21.3, 7.5, 27.9),
    "SW2": (50.0, 21.3, 57.6, 27.9),
    "U1": (30.4, 6.4, 39.6, 15.6),
    "U2": (40.6, 3.8, 48.4, 11.2),
    "U3": (26.8, 21.6, 31.2, 25.6),
    "U4": (19.8, 21.4, 24.2, 25.0),
    "J4": (23.5, 27.0, 33.6, 30.0),
    "Y1": (25.3, 11.2, 29.7, 14.8),
}

# Allowed centre regions for the packed parts.
REGIONS = [
    (1.4, 5.0, 29.6, 16.8),
    (39.2, 5.0, 50.2, 16.8),
    (1.4, 21.5, 56.2, 23.6),
    (1.4, 23.6, 7.0, 30.4),
    (49.0, 27.8, 56.2, 30.4),
    (18.0, 23.6, 38.8, 30.4),
]

SIZE_0603 = (3.2, 1.8)
SIZE_0805 = (4.0, 2.2)
SIZE_SOD = (3.8, 2.0)
SIZE_SOT = (4.0, 3.2)
SIZE_L = (4.0, 2.6)


def passive_size(ref, fpname):
    if fpname.startswith("C_0805"):
        return SIZE_0805
    if fpname.startswith("D_SOD"):
        return SIZE_SOD
    if fpname.startswith("SOT-23-6"):
        return SIZE_SOT
    if fpname.startswith("L_pol"):
        return SIZE_L
    return SIZE_0603


def pack_passives(parts):
    """Return ref -> (x, y) for every non-fixed part, without overlaps."""
    boxes = []
    for name, (x0, y0, x1, y1) in FIXED_BOX.items():
        boxes.append((x0, y0, x1, y1))

    # Candidate centres on a 0.4 mm lattice inside the allowed regions.
    cand = []
    for x0, y0, x1, y1 in REGIONS:
        x = x0
        while x <= x1:
            y = y0
            while y <= y1:
                cand.append((round(x, 2), round(y, 2)))
                y += 0.4
            x += 0.4

    def free(cx, cy, w, h):
        x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
        if x0 < 1.0 or y0 < 1.0 or x1 > W - 1.0 or y1 > H - 1.0:
            return False
        for bx0, by0, bx1, by1 in boxes:
            if x0 < bx1 and x1 > bx0 and y0 < by1 and y1 > by0:
                return False
        return True

    result = {}
    # Place larger parts first.
    order = sorted(
        [p for p in parts if p["ref"] not in FIXED],
        key=lambda p: -(passive_size(p["ref"], p["fp"].split(":", 1)[1])[0]
                        * passive_size(p["ref"], p["fp"].split(":", 1)[1])[1]),
    )
    for part in order:
        w, h = passive_size(part["ref"], part["fp"].split(":", 1)[1])
        px, py, _ = PLACE[part["ref"]]
        best = None
        best_d = None
        for cx, cy in cand:
            if free(cx, cy, w, h):
                d = (cx - px) ** 2 + (cy - py) ** 2
                if best_d is None or d < best_d:
                    best_d = d
                    best = (cx, cy)
        if best is None:
            raise RuntimeError("no room for " + part["ref"])
        cx, cy = best
        result[part["ref"]] = (cx, cy)
        boxes.append((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2))
    return result


SIG_W = 0.2
PWR_W = 0.3
VIA_D = 0.5
VIA_DRILL = 0.3


def P(x, y):
    return pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y))


def board_points(inset=0.0):
    left, right = inset, W - inset
    top, bottom = inset, H - inset
    leg = CHAMFER - inset * (2.0 - math.sqrt(2.0))
    return [
        (right, top + leg), (right, bottom - leg), (right - leg, bottom),
        (left + leg, bottom), (left, bottom - leg), (left, top + leg),
        (left + leg, top), (right - leg, top),
    ]


class Builder:
    def __init__(self):
        self.board = pcbnew.BOARD()
        self.board.SetCopperLayerCount(4)
        ds = self.board.GetDesignSettings()
        ds.SetBoardThickness(pcbnew.FromMM(THICKNESS))
        ds.m_CopperEdgeClearance = pcbnew.FromMM(0.15)
        ds.m_MinSilkTextHeight = pcbnew.FromMM(0.5)
        ds.m_MinSilkTextThickness = pcbnew.FromMM(0.08)
        ds.m_MinClearance = pcbnew.FromMM(0.15)
        ds.m_TrackMinWidth = pcbnew.FromMM(0.1)
        ds.m_ViasMinSize = pcbnew.FromMM(0.35)
        ds.m_ViasMinAnnularWidth = pcbnew.FromMM(0.1)
        ds.SetAuxOrigin(P(0, H))
        self.nets = {}
        self.pads = {}
        self._add_nets()
        self._place()

    def _add_nets(self):
        names = sorted({n for p in PARTS for n in p["pins"].values() if n})
        for name in names:
            ni = pcbnew.NETINFO_ITEM(self.board, name)
            self.board.Add(ni)
            self.nets[name] = ni
        self.nets[GND] = self.board.FindNet(GND)
        self.nets[VSYS] = self.board.FindNet(VSYS)
        self.nets[P3V3] = self.board.FindNet(P3V3)
        self.nets[P1V1] = self.board.FindNet(P1V1)

    def _place(self):
        packed = pack_passives(PARTS)
        for part in PARTS:
            if part["ref"] in packed:
                x, y = packed[part["ref"]]
                rot = 0
            else:
                x, y, rot = PLACE[part["ref"]]
            fpname = part["fp"].split(":", 1)[1]
            fp = pcbnew.FootprintLoad(FP_DIR, fpname)
            if fp is None:
                raise RuntimeError("footprint not found: " + fpname)
            fp.SetPosition(P(x, y))
            fp.SetOrientationDegrees(rot)
            self.board.Add(fp)
            fp.SetReference(part["ref"])
            fp.SetValue(part["value"])
            fp.Reference().SetVisible(False)
            fp.Value().SetVisible(False)
            if part["ref"] in ("J1", "J2", "J3"):
                for g in fp.GraphicalItems():
                    if g.GetLayer() == pcbnew.F_SilkS:
                        g.SetLayer(pcbnew.F_Fab)
            for pad in fp.Pads():
                num = pad.GetNumber()
                pad.SetLocalSolderMaskMargin(0)
                net = part["pins"].get(num)
                if net:
                    pad.SetNet(self.nets[net])
                if net == GND:
                    pad.SetLocalZoneConnection(pcbnew.ZONE_CONNECTION_FULL)
                self.pads[(part["ref"], num)] = pad

    def outline(self):
        pts = board_points()
        for a, b in zip(pts, pts[1:] + pts[:1]):
            seg = pcbnew.PCB_SHAPE(self.board)
            seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
            seg.SetLayer(pcbnew.Edge_Cuts)
            seg.SetStart(P(*a))
            seg.SetEnd(P(*b))
            seg.SetWidth(pcbnew.FromMM(0.1))
            self.board.Add(seg)

    def texts(self):
        def text(s, x, y, size=0.8, w=0.12, layer=pcbnew.F_SilkS,
                 angle=0.0):
            t = pcbnew.PCB_TEXT(self.board)
            t.SetText(s)
            t.SetPosition(P(x, y))
            t.SetLayer(layer)
            t.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(size), pcbnew.FromMM(size)))
            t.SetTextThickness(pcbnew.FromMM(w))
            t.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_CENTER)
            t.SetTextAngleDegrees(angle)
            if layer == pcbnew.B_SilkS:
                t.SetMirrored(True)
            self.board.Add(t)

        # board title
        text("PICO2-COMPAT  RP2350A", 16.0, 6.2, 1.0, 0.15, layer=pcbnew.B_SilkS)
        

        # header pin labels
        for n, label in HEADER_LABELS.items():
            if n <= 20:
                x = 1.37 + (20 - n) * 2.54
                y = 3.8
            else:
                x = 1.37 + (n - 21) * 2.54
                y = 18.7
            text(label, x, y, 0.55, 0.09)

        # connector labels
        text("NATIVE USB", 53.0, 5.0, 0.7, 0.11, angle=90)
        text("PIO USB", 12.5, 26.6, 0.7, 0.11)
        text("UART", 44.5, 26.6, 0.7, 0.11)
        text("BOOT", 4.0, 26.8, 0.7, 0.11)
        text("RUN", 53.8, 26.5, 0.7, 0.11)

        # warnings / notes
        text("PIO USB: 1.5k D+ pull-up fitted - device mode only", 30.0, 10.0, 0.55, 0.08, layer=pcbnew.B_SilkS)
        text("VSYS 3.8-5.5V for 3.3V LDO", 30.0, 12.0, 0.55, 0.08, layer=pcbnew.B_SilkS)

        # pin 1 marker for the header
        text("1", 50.2, 0.8, 0.9, 0.15)

        # bottom silkscreen title
        


def main():
    b = Builder()
    b.outline()
    b.texts()
    path = os.path.join(ROOT, f"{PROJECT}.kicad_pcb")
    pcbnew.SaveBoard(path, b.board)
    print("wrote", path)


if __name__ == "__main__":
    main()
