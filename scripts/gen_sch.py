"""Generate pico2-compat.kicad_sch (KiCad 10 compatible S-expression)."""

import os
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from design import PROJECT, SYMBOLS, PASSIVES, PARTS, POWER_FLAGS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_UUID = "7c1f0e52-3b7a-4e2d-9a51-0c7d4b3a2f10"


def u():
    return str(uuid.uuid4())


def fmt(v):
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    return s if s not in ("", "-0") else "0"


def symbol_pins(sym):
    if sym in SYMBOLS:
        return SYMBOLS[sym]["pins"], SYMBOLS[sym]["halfw"], SYMBOLS[sym]["height"]
    return PASSIVES[sym]["pins"], 1.27, 1.27


def graphic(name, sym):
    if sym in SYMBOLS:
        hw = SYMBOLS[sym]["halfw"]
        hh = SYMBOLS[sym]["height"]
        return (
            f'      (rectangle (start {fmt(-hw)} {fmt(hh)}) (end {fmt(hw)} {fmt(-hh)}) '
            f'(stroke (width 0.254) (type default)) (fill (type background)))\n'
        )
    if sym in ("R", "C", "L"):
        return (
            '      (rectangle (start -2.54 1.016) (end 2.54 -1.016) '
            '(stroke (width 0.254) (type default)) (fill (type none)))\n'
        )
    if sym in ("D", "LED"):
        s = (
            '      (polyline (pts (xy -1.27 1.27) (xy -1.27 -1.27) (xy 1.27 0) (xy -1.27 1.27)) '
            '(stroke (width 0.254) (type default)) (fill (type none)))\n'
            '      (polyline (pts (xy 1.27 1.27) (xy 1.27 -1.27)) '
            '(stroke (width 0.254) (type default)) (fill (type none)))\n'
        )
        if sym == "LED":
            s += (
                '      (polyline (pts (xy -0.5 2.0) (xy 0.6 3.1)) (stroke (width 0.2) (type default)) (fill (type none)))\n'
                '      (polyline (pts (xy 0.6 3.1) (xy 0.1 2.9) (xy 0.4 2.4) (xy 0.6 3.1)) (stroke (width 0.2) (type default)) (fill (type none)))\n'
                '      (polyline (pts (xy 0.5 2.0) (xy 1.6 3.1)) (stroke (width 0.2) (type default)) (fill (type none)))\n'
                '      (polyline (pts (xy 1.6 3.1) (xy 1.1 2.9) (xy 1.4 2.4) (xy 1.6 3.1)) (stroke (width 0.2) (type default)) (fill (type none)))\n'
            )
        return s
    if sym == "PWR_FLAG":
        return (
            '      (polyline (pts (xy 0 0) (xy 0 1.27) (xy -0.762 1.27) (xy 0 2.54) (xy 0.762 1.27) (xy 0 1.27)) '
            '(stroke (width 0.254) (type default)) (fill (type none)))\n'
        )
    raise ValueError(sym)


PWR_FLAG_BLOCK = r"""    (symbol "pico2:PWR_FLAG"
        (power global)
        (pin_numbers
            (hide yes)
        )
        (pin_names
            (offset 0)
            (hide yes)
        )
        (exclude_from_sim no)
        (in_bom yes)
        (on_board yes)
        (in_pos_files yes)
        (duplicate_pin_numbers_are_jumpers no)
        (property "Reference" "#FLG"
            (at 0 1.905 0)
            (show_name no)
            (do_not_autoplace no)
            (hide yes)
            (effects
                (font
                    (size 1.27 1.27)
                )
            )
        )
        (property "Value" "PWR_FLAG"
            (at 0 3.81 0)
            (show_name no)
            (do_not_autoplace no)
            (effects
                (font
                    (size 1.27 1.27)
                )
            )
        )
        (property "Footprint" ""
            (at 0 0 0)
            (show_name no)
            (do_not_autoplace no)
            (hide yes)
            (effects
                (font
                    (size 1.27 1.27)
                )
            )
        )
        (property "Datasheet" ""
            (at 0 0 0)
            (show_name no)
            (do_not_autoplace no)
            (hide yes)
            (effects
                (font
                    (size 1.27 1.27)
                )
            )
        )
        (property "Description" "Special symbol for telling ERC where power comes from"
            (at 0 0 0)
            (show_name no)
            (do_not_autoplace no)
            (hide yes)
            (effects
                (font
                    (size 1.27 1.27)
                )
            )
        )
        (property "ki_keywords" "flag power"
            (at 0 0 0)
            (show_name no)
            (do_not_autoplace no)
            (hide yes)
            (effects
                (font
                    (size 1.27 1.27)
                )
            )
        )
        (symbol "PWR_FLAG_0_0"
            (pin power_out line
                (at 0 0 90)
                (length 0)
                (name ""
                    (effects
                        (font
                            (size 1.27 1.27)
                        )
                    )
                )
                (number "1"
                    (effects
                        (font
                            (size 1.27 1.27)
                        )
                    )
                )
            )
        )
        (symbol "PWR_FLAG_0_1"
            (polyline
                (pts
                    (xy 0 0) (xy 0 1.27) (xy -1.016 1.905) (xy 0 2.54) (xy 1.016 1.905) (xy 0 1.27)
                )
                (stroke
                    (width 0)
                    (type default)
                )
                (fill
                    (type none)
                )
            )
        )
        (embedded_fonts no)
    )
"""

def lib_symbol(sym):
    if sym == "PWR_FLAG":
        return PWR_FLAG_BLOCK
    pins, hw, hh = symbol_pins(sym)
    s = f'''    (symbol "pico2:{sym}"
      {"(power global)" if sym == "PWR_FLAG" else ""}
      (pin_names (offset 1.016))
      (exclude_from_sim no)
      (in_bom yes)
      (on_board yes)
      (property "Reference" "U" (at 0 {fmt(hh + 2.54)} 0) (effects (font (size 1.27 1.27))))
      (property "Value" "{sym}" (at 0 {fmt(-hh - 2.54)} 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (property "LCSC" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol "{sym}_0_1"
{graphic(sym, sym)}      )
      (symbol "{sym}_1_1"
'''
    for side, num, pname, etype, y in pins:
        if side == "L":
            x, ang = -hw - 2.54, 0
        elif side == "R":
            x, ang = hw + 2.54, 180
        elif side == "B":
            x, ang = 0, 90
        else:
            raise ValueError(side)
        plen = 0 if sym == "PWR_FLAG" else 2.54
        s += (
            f'        (pin {etype} line (at {fmt(x)} {fmt(y)} {ang}) (length {plen})\n'
            f'          (name "{pname}" (effects (font (size 1.27 1.27))))\n'
            f'          (number "{num}" (effects (font (size 1.27 1.27)))))\n'
        )
    s += "      )\n    )\n"
    return s


# Manual placement for the large parts; the passives are placed on a grid.
LAYOUT = {
    "U1": (247.65, 219.71),
    "J5A": (99.06, 180.34),
    "J5B": (99.06, 260.35),
    "U3": (429.26, 219.71),
    "U2": (349.25, 80.01),
    "J1": (500.38, 419.10),
    "J2": (99.06, 419.10),
    "J3": (299.72, 419.10),
    "U4": (60.96, 500.38),
    "Y1": (419.10, 80.01),
    "J4": (549.91, 520.70),
    "SW1": (60.96, 599.44),
    "SW2": (110.49, 599.44),
}

STUB = 3.81


def auto_layout():
    """Place the remaining two-pin parts on a regular grid."""
    placed = set(LAYOUT)
    grid = []
    for part in PARTS:
        if part["ref"] in placed:
            continue
        grid.append(part["ref"])
    x0, y0 = 50.80, 495.30
    dx, dy = 40.64, 25.40
    per_row = 12
    for i, ref in enumerate(grid):
        LAYOUT[ref] = (x0 + (i % per_row) * dx, y0 + (i // per_row) * dy)


def pin_sheet_pos(sx, sy, side, x, y):
    # library +Y is up, schematic +Y is down
    return (sx + x, sy - y)


def main():
    auto_layout()
    out = []
    out.append("(kicad_sch\n")
    out.append("  (version 20231120)\n")
    out.append('  (generator "eeschema")\n')
    out.append('  (generator_version "8.0")\n')
    out.append(f'  (uuid "{ROOT_UUID}")\n')
    out.append('  (paper "A1")\n')
    out.append("  (title_block\n")
    out.append('    (title "Pico 2 compatible RP2350A board")\n')
    out.append('    (rev "A")\n')
    out.append('    (comment 1 "57.6 x 31.4 mm, Pico-compatible 2x20 header, 3x USB Type-C")\n')
    out.append('    (comment 2 "Native USB + CH343P UART0 + PIO USB on GP12/GP13")\n')
    out.append('    (comment 3 "BOOT and RUN buttons, 3.3 V LDO, RP2350 internal 1.1 V regulator")\n')
    out.append("  )\n")

    used = []
    for part in PARTS:
        if part["sym"] not in used:
            used.append(part["sym"])
    out.append("  (lib_symbols\n")
    for sym in used:
        out.append(lib_symbol(sym))
    if "PWR_FLAG" not in used:
        out.append(lib_symbol("PWR_FLAG"))
    out.append("  )\n")

    # Design notes
    notes = [
        ("Pico 2 header: pin 1 = GP0 at the native-USB end; 2.54 mm pitch, 17.78 mm row spacing.", 30, 40),
        ("UART0: GP0 (TX, pin 1) -> CH343P RXD (pin 5); CH343P TXD (pin 4) -> GP1 (RX, pin 2).", 30, 47),
        ("PIO USB: GP12 (pin 16) = D+, GP13 (pin 17) = D-, 22 ohm series; HOST port (CC 56k Rp, VBUS from NATIVE USB).", 30, 54),
        ("Native USB: RP2350 USB_DP/USB_DM, 27 ohm series, USBLC6 ESD.", 30, 61),
        ("Power: NATIVE/UART VBUS are diode-ORed to VSYS; AP2112K-3.3 makes 3V3. PIO VBUS is an output from NATIVE VBUS.", 30, 68),
        ("BOOT: QSPI_SS --1k--> button --> GND. RUN: RUN --1k--> button --> GND.", 30, 75),
    ]
    for text, x, y in notes:
        out.append(f'  (text "{text}" (at {x} {y} 0) (effects (font (size 1.5 1.5))))\n')

    for part in PARTS:
        sx, sy = LAYOUT[part["ref"]]
        pins, hw, hh = symbol_pins(part["sym"])
        out.append(f'  (symbol (lib_id "pico2:{part["sym"]}") (at {fmt(sx)} {fmt(sy)} 0) (unit 1)\n')
        out.append("    (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)\n")
        out.append(f'    (uuid "{u()}")\n')
        out.append(f'    (property "Reference" "{part["ref"]}" (at {fmt(sx)} {fmt(sy - hh - 4.5)} 0) (effects (font (size 1.27 1.27))))\n')
        out.append(f'    (property "Value" "{part["value"]}" (at {fmt(sx)} {fmt(sy - hh - 1.8)} 0) (effects (font (size 1.27 1.27))))\n')
        out.append(f'    (property "Footprint" "{part["fp"]}" (at {fmt(sx)} {fmt(sy)} 0) (effects (font (size 1.27 1.27)) hide))\n')
        out.append(f'    (property "Datasheet" "" (at {fmt(sx)} {fmt(sy)} 0) (effects (font (size 1.27 1.27)) hide))\n')
        out.append(f'    (property "LCSC" "{part["lcsc"]}" (at {fmt(sx)} {fmt(sy)} 0) (effects (font (size 1.27 1.27)) hide))\n')
        for side, num, pname, etype, y in pins:
            out.append(f'    (pin "{num}" (uuid "{u()}"))\n')
        out.append(f'    (instances (project "{PROJECT}" (path "/{ROOT_UUID}" (reference "{part["ref"]}") (unit 1))))\n')
        out.append("  )\n")

        for side, num, pname, etype, y in pins:
            if part["sym"] in SYMBOLS:
                hw2 = SYMBOLS[part["sym"]]["halfw"]
                lx = -hw2 - 2.54 if side == "L" else hw2 + 2.54
            else:
                lx = -3.81 if side == "L" else 3.81
            px, py = pin_sheet_pos(sx, sy, side, lx, y)
            net = part["pins"].get(str(num))
            if net is None:
                out.append(f'  (no_connect (at {fmt(px)} {fmt(py)}) (uuid "{u()}"))\n')
                continue
            if side == "L":
                ex = px - STUB
                just = "right"
            elif side == "R":
                ex = px + STUB
                just = "left"
            else:
                ey = py + STUB
                ex, just = px, "left"
            if side == "B":
                out.append(f'  (wire (pts (xy {fmt(px)} {fmt(py)}) (xy {fmt(ex)} {fmt(py + STUB)})) (stroke (width 0) (type default)) (uuid "{u()}"))\n')
                out.append(f'  (label "{net}" (at {fmt(ex)} {fmt(py + STUB)} 0) (effects (font (size 1.27 1.27)) (justify {just} bottom)) (uuid "{u()}"))\n')
            else:
                out.append(f'  (wire (pts (xy {fmt(px)} {fmt(py)}) (xy {fmt(ex)} {fmt(py)})) (stroke (width 0) (type default)) (uuid "{u()}"))\n')
                out.append(f'  (label "{net}" (at {fmt(ex)} {fmt(py)} 0) (effects (font (size 1.27 1.27)) (justify {just} bottom)) (uuid "{u()}"))\n')

    # PWR_FLAGs
    for i, (net, ref) in enumerate(POWER_FLAGS):
        sx, sy = 30.48 + i * 35.56, 787.40
        out.append(f'  (symbol (lib_id "pico2:PWR_FLAG") (at {fmt(sx)} {fmt(sy)} 0) (unit 1)\n')
        out.append("    (exclude_from_sim no) (in_bom no) (on_board no) (dnp no)\n")
        out.append(f'    (uuid "{u()}")\n')
        out.append(f'    (property "Reference" "{ref}" (at {fmt(sx)} {fmt(sy - 3)} 0) (effects (font (size 1.27 1.27)) hide))\n')
        out.append(f'    (property "Value" "PWR_FLAG" (at {fmt(sx)} {fmt(sy + 4)} 0) (effects (font (size 1.27 1.27))))\n')
        out.append(f'    (property "Footprint" "" (at {fmt(sx)} {fmt(sy)} 0) (effects (font (size 1.27 1.27)) hide))\n')
        out.append(f'    (property "Datasheet" "" (at {fmt(sx)} {fmt(sy)} 0) (effects (font (size 1.27 1.27)) hide))\n')
        out.append(f'    (pin "1" (uuid "{u()}"))\n')
        out.append(f'    (instances (project "{PROJECT}" (path "/{ROOT_UUID}" (reference "{ref}") (unit 1))))\n')
        out.append("  )\n")
        out.append(f'  (wire (pts (xy {fmt(sx)} {fmt(sy)}) (xy {fmt(sx)} {fmt(sy + STUB)})) (stroke (width 0) (type default)) (uuid "{u()}"))\n')
        out.append(f'  (label "{net}" (at {fmt(sx)} {fmt(sy + STUB)} 0) (effects (font (size 1.27 1.27)) (justify left bottom)) (uuid "{u()}"))\n')

    out.append('  (sheet_instances (path "/" (page "1")))\n')
    out.append(")\n")

    path = os.path.join(ROOT, f"{PROJECT}.kicad_sch")
    with open(path, "w") as f:
        f.write("".join(out))
    print("wrote", path)

    # Standalone symbol library for editing
    symlib = ["(kicad_symbol_lib (version 20231120) (generator \"kicad_symbol_editor\") (generator_version \"8.0\")\n"]
    for sym in used + ["PWR_FLAG"]:
        symlib.append(lib_symbol(sym).replace(f'"pico2:{sym}"', f'"{sym}"'))
    symlib.append(")\n")
    os.makedirs(os.path.join(ROOT, "lib"), exist_ok=True)
    with open(os.path.join(ROOT, "lib", "pico2.kicad_sym"), "w") as f:
        f.write("".join(symlib))

    with open(os.path.join(ROOT, "fp-lib-table"), "w") as f:
        f.write('(fp_lib_table\n  (version 7)\n  (lib (name "PICO2")(type "KiCad")(uri "${KIPRJMOD}/lib/PICO2.pretty")(options "")(descr "pico2-compat footprints"))\n)\n')
    with open(os.path.join(ROOT, "sym-lib-table"), "w") as f:
        f.write('(sym_lib_table\n  (version 7)\n  (lib (name "pico2")(type "KiCad")(uri "${KIPRJMOD}/lib/pico2.kicad_sym")(options "")(descr "pico2-compat symbols"))\n)\n')


if __name__ == "__main__":
    main()
