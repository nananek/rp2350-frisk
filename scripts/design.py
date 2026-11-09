"""Single source of truth for the pico2-compat board.

The schematic and the PCB generator both import this module, so the netlist
cannot drift between the two.  The board is a Raspberry Pi Pico 2 equivalent
with:

* the same 57.6 x 31.4 mm outline as nananek/serial-km-emulator,
* a Pico-compatible 2x20 GPIO header (2.54 mm pitch, 17.78 mm row spacing),
* three USB Type-C ports (native RP2350 USB, CH343P UART, PIO USB),
* separate BOOT and RUN buttons,
* a 3.3 V LDO and the RP2350 internal 1.1 V regulator.

Net names are deliberately functional so that the schematic labels read like
the Pico pin names.
"""

PROJECT = "pico2-compat"
REPO_URL = "https://github.com/nananek/pico2-compat"

# ---------------------------------------------------------------------------
# Symbols (library coordinates: +Y up, as in .kicad_sym files)
# ---------------------------------------------------------------------------

GND = "GND"
VSYS = "VSYS"
P3V3 = "3V3"
P1V1 = "1V1"

def lr(left, right, halfw=15.24, pitch=2.54, margin=2.54):
    """Build a rectangular symbol with pins on the left and right sides.

    ``left`` and ``right`` are lists of ``(number, name, electrical_type)``.
    Pins are spaced 2.54 mm apart and start at the top of the rectangle.
    """
    n = max(len(left), len(right))
    top = (n - 1) * pitch / 2.0
    height = top + margin
    pins = []
    for i, (num, name, etype) in enumerate(left):
        pins.append(("L", num, name, etype, top - i * pitch))
    for i, (num, name, etype) in enumerate(right):
        pins.append(("R", num, name, etype, top - i * pitch))
    return dict(halfw=halfw, height=height, pins=pins)


# Pico-compatible header.  Pin 1 is at the USB end (right end of the board)
# and pins 1..20 run along one 0.7 inch row; pins 21..40 run back along the
# other row.  The schematic symbol groups them 1..20 / 21..40.
HEADER_PINS = [
    (1, "GP0", "bidirectional"), (2, "GP1", "bidirectional"), (3, "GND", "power_in"),
    (4, "GP2", "bidirectional"), (5, "GP3", "bidirectional"), (6, "GP4", "bidirectional"),
    (7, "GP5", "bidirectional"), (8, "GND", "power_in"), (9, "GP6", "bidirectional"),
    (10, "GP7", "bidirectional"), (11, "GP8", "bidirectional"), (12, "GP9", "bidirectional"),
    (13, "GND", "power_in"), (14, "GP10", "bidirectional"), (15, "GP11", "bidirectional"),
    (16, "GP12", "bidirectional"), (17, "GP13", "bidirectional"), (18, "GND", "power_in"),
    (19, "GP14", "bidirectional"), (20, "GP15", "bidirectional"),
    (21, "GP16", "bidirectional"), (22, "GP17", "bidirectional"), (23, "GND", "power_in"),
    (24, "GP18", "bidirectional"), (25, "GP19", "bidirectional"), (26, "GP20", "bidirectional"),
    (27, "GP21", "bidirectional"), (28, "GND", "power_in"), (29, "GP22", "bidirectional"),
    (30, "RUN", "input"), (31, "GP26", "bidirectional"), (32, "GP27", "bidirectional"),
    (33, "GND", "power_in"), (34, "GP28", "bidirectional"), (35, "ADC_VREF", "power_in"),
    (36, "3V3", "power_out"), (37, "3V3_EN", "input"), (38, "GND", "power_in"),
    (39, "VSYS", "power_in"), (40, "VBUS", "power_in"),
]
# The header is a connector: its power pins are passive from the schematic
# point of view.  The board side (RP2350/regulator) still has power_in pins.
_PASSIVE_HEADER = {"GND", "ADC_VREF", "3V3", "3V3_EN", "VSYS", "VBUS", "RUN"}
HEADER_PINS = [
    (n, name, "passive" if name in _PASSIVE_HEADER else etype)
    for n, name, etype in HEADER_PINS
]

RP_LEFT = [
    (2, "GPIO0", "bidirectional"), (3, "GPIO1", "bidirectional"),
    (4, "GPIO2", "bidirectional"), (5, "GPIO3", "bidirectional"),
    (7, "GPIO4", "bidirectional"), (8, "GPIO5", "bidirectional"),
    (9, "GPIO6", "bidirectional"), (10, "GPIO7", "bidirectional"),
    (12, "GPIO8", "bidirectional"), (13, "GPIO9", "bidirectional"),
    (14, "GPIO10", "bidirectional"), (15, "GPIO11", "bidirectional"),
    (16, "GPIO12", "bidirectional"), (17, "GPIO13", "bidirectional"),
    (18, "GPIO14", "bidirectional"), (19, "GPIO15", "bidirectional"),
    (27, "GPIO16", "bidirectional"), (28, "GPIO17", "bidirectional"),
    (29, "GPIO18", "bidirectional"), (31, "GPIO19", "bidirectional"),
    (32, "GPIO20", "bidirectional"), (33, "GPIO21", "bidirectional"),
    (34, "GPIO22", "bidirectional"), (35, "GPIO23", "bidirectional"),
    (36, "GPIO24", "bidirectional"), (37, "GPIO25", "bidirectional"),
    (40, "GPIO26_ADC0", "bidirectional"), (41, "GPIO27_ADC1", "bidirectional"),
    (42, "GPIO28_ADC2", "bidirectional"), (43, "GPIO29_ADC3", "bidirectional"),
]
RP_RIGHT = [
    (1, "IOVDD", "power_in"), (6, "DVDD", "power_in"),
    (11, "IOVDD", "power_in"), (20, "IOVDD", "power_in"),
    (21, "XIN", "input"), (22, "XOUT", "output"),
    (23, "DVDD", "power_in"), (24, "SWCLK", "input"), (25, "SWDIO", "bidirectional"),
    (26, "RUN", "input"), (30, "IOVDD", "power_in"), (38, "IOVDD", "power_in"),
    (39, "DVDD", "power_in"), (44, "ADC_AVDD", "power_in"),
    (45, "IOVDD", "power_in"), (46, "VREG_AVDD", "power_in"),
    (47, "VREG_PGND", "power_in"), (48, "VREG_LX", "power_out"),
    (49, "VREG_VIN", "power_in"), (50, "VREG_FB", "power_in"),
    (51, "USB_DM", "bidirectional"), (52, "USB_DP", "bidirectional"),
    (53, "USB_OTP_VDD", "power_in"), (54, "QSPI_IOVDD", "power_in"),
    (55, "QSPI_SD3", "bidirectional"), (56, "QSPI_SCLK", "output"),
    (57, "QSPI_SD0", "bidirectional"), (58, "QSPI_SD2", "bidirectional"),
    (59, "QSPI_SD1", "bidirectional"), (60, "QSPI_SS", "output"),
    (61, "GND", "power_in"),
]

SYMBOLS = {
    "RP2350A": lr(RP_LEFT, RP_RIGHT, halfw=30.48, margin=5.08),
    "PICO_HEADER_TOP": lr(
        [(n, name, etype) for n, name, etype in HEADER_PINS[:20]],
        [], halfw=12.7, margin=3.81,
    ),
    "PICO_HEADER_BOTTOM": lr(
        [(n, name, etype) for n, name, etype in HEADER_PINS[20:]],
        [], halfw=12.7, margin=3.81,
    ),
    "W25Q32": lr(
        [(1, "~CS", "input"), (2, "DO/IO1", "bidirectional"),
         (3, "~WP/IO2", "bidirectional"), (4, "GND", "power_in")],
        [(8, "VCC", "power_in"), (7, "~HOLD/IO3", "bidirectional"),
         (6, "CLK", "input"), (5, "DI/IO0", "bidirectional")],
        halfw=11.43, margin=3.81,
    ),
    "CH343P": lr(
        [(1, "VIO", "power_in"), (2, "GND", "power_in"), (3, "VDD5", "power_in"),
         (4, "TXD", "output"), (5, "RXD", "input"), (6, "V3", "power_out"),
         (7, "UD+", "bidirectional"), (8, "UD-", "bidirectional"), (9, "VBUS", "input")],
        [(17, "EP/GND", "power_in"), (16, "RI", "input"), (15, "CTS", "input"),
         (14, "DSR", "input"), (13, "RTS", "output"), (12, "DTR", "output"),
         (11, "DCD", "input"), (10, "ACT#", "output")],
        halfw=13.97, margin=3.81,
    ),
    "AP2112K": lr(
        [(1, "VIN", "power_in"), (2, "GND", "power_in"), (3, "EN", "input")],
        [(5, "VOUT", "power_out"), (4, "NC", "no_connect")],
        halfw=10.16, margin=3.81,
    ),
    "USB_C": lr(
        [("A4", "VBUS", "passive"), ("A9", "VBUS", "passive"),
         ("B4", "VBUS", "passive"), ("B9", "VBUS", "passive"),
         ("A1", "GND", "passive"), ("A12", "GND", "passive"),
         ("B1", "GND", "passive"), ("B12", "GND", "passive"),
         ("SH", "SHIELD", "passive")],
        [("A5", "CC1", "passive"), ("B5", "CC2", "passive"),
         ("A6", "D+", "passive"), ("B6", "D+", "passive"),
         ("A7", "D-", "passive"), ("B7", "D-", "passive"),
         ("A8", "SBU1", "passive"), ("B8", "SBU2", "passive")],
        halfw=15.24, margin=3.81,
    ),
    "USBLC6": lr(
        [(1, "I/O1", "bidirectional"), (2, "GND", "power_in"), (3, "I/O2", "bidirectional")],
        [(6, "I/O1", "bidirectional"), (5, "VBUS", "passive"), (4, "I/O2", "bidirectional")],
        halfw=8.89, margin=3.81,
    ),
    "CRYSTAL": lr(
        [(1, "XIN", "passive"), (2, "GND", "power_in")],
        [(4, "GND", "power_in"), (3, "XOUT", "passive")],
        halfw=8.89, margin=3.81,
    ),
    "SW": lr(
        [(1, "A", "passive")],
        [(2, "B", "passive")],
        halfw=6.35, margin=2.54,
    ),
    "DEBUG": lr(
        [(1, "SWCLK", "passive"), (2, "GND", "passive"), (3, "SWDIO", "passive")],
        [], halfw=8.89, margin=3.81,
    ),
}

PASSIVES = {
    "R": dict(pins=[("L", "1", "~", "passive", 0.0), ("R", "2", "~", "passive", 0.0)]),
    "C": dict(pins=[("L", "1", "~", "passive", 0.0), ("R", "2", "~", "passive", 0.0)]),
    "D": dict(pins=[("L", "2", "A", "passive", 0.0), ("R", "1", "K", "passive", 0.0)]),
    "LED": dict(pins=[("L", "2", "A", "passive", 0.0), ("R", "1", "K", "passive", 0.0)]),
    "L": dict(pins=[("L", "1", "~", "passive", 0.0), ("R", "2", "~", "passive", 0.0)]),
    "PWR_FLAG": dict(pins=[("B", "1", "pwr", "power_out", 0.0)]),
}

# ---------------------------------------------------------------------------
# Parts
# ---------------------------------------------------------------------------
# footprint names are relative to lib/PICO2.pretty
parts = []

def part(ref, value, sym, fp, lcsc, pins, fitted=True):
    parts.append(dict(ref=ref, value=value, sym=sym, fp="PICO2:" + fp,
                      lcsc=lcsc, pins=pins, fitted=fitted))

# --- RP2350A and its support ------------------------------------------------
part("U1", "RP2350A", "RP2350A",
     "RP2350-QFN-60-1EP_7x7_P0.4mm_EP3.4x3.4mm_ThermalVias", "C42411118", {
    "1": P3V3, "2": "UART0_TX", "3": "UART0_RX", "4": "GPIO2", "5": "GPIO3",
    "6": P1V1, "7": "GPIO4", "8": "GPIO5", "9": "GPIO6", "10": "GPIO7",
    "11": P3V3, "12": "GPIO8", "13": "GPIO9", "14": "GPIO10", "15": "GPIO11",
    "16": "PIO_DP", "17": "PIO_DM", "18": "GPIO14", "19": "GPIO15", "20": P3V3,
    "21": "XIN", "22": "XOUT", "23": None, "24": "SWCLK", "25": "SWDIO",
    "26": "RUN", "27": "GPIO16", "28": "GPIO17", "29": "GPIO18", "30": P3V3,
    "31": "GPIO19", "32": "GPIO20", "33": "GPIO21", "34": "GPIO22",
    "35": None, "36": None, "37": None, "38": P3V3, "39": P1V1,
    "40": "GPIO26", "41": "GPIO27", "42": "GPIO28", "43": None,
    "44": P3V3, "45": P3V3, "46": "VREG_AVDD", "47": GND, "48": "VREG_LX",
    "49": P3V3, "50": P1V1, "51": "USB_DM", "52": "USB_DP", "53": P3V3,
    "54": P3V3, "55": "QSPI_SD3", "56": "QSPI_SCLK", "57": "QSPI_SD0",
    "58": "QSPI_SD2", "59": "QSPI_SD1", "60": "QSPI_SS", "61": GND,
})

part("U2", "W25Q32JVSSIQ", "W25Q32", "SOIC-8_5.3x5.3mm_P1.27mm", "C179173", {
    "1": "FLASH_CS", "2": "QSPI_SD1", "3": "QSPI_SD2", "4": GND,
    "5": "QSPI_SD0", "6": "QSPI_SCLK", "7": "QSPI_SD3", "8": P3V3,
})

part("U3", "CH343P", "CH343P", "QFN-16-1EP_3x3mm_P0.5mm_EP1.7x1.7mm", "C2846043", {
    "1": P3V3, "2": GND, "3": VSYS, "4": "UART0_RX", "5": "UART0_TX",
    "6": "V3_343", "7": "UART_DP_CONN", "8": "UART_DM_CONN", "9": "VBUS_UART",
    "10": "UART_ACT", "11": None, "12": None, "13": None, "14": None,
    "15": None, "16": None, "17": GND,
})

part("U4", "AP2112K-3.3", "AP2112K", "SOT-23-5", "C51118", {
    "1": VSYS, "2": GND, "3": "3V3_EN", "4": None, "5": P3V3,
})

# --- USB Type-C ports -------------------------------------------------------
# J1 = native RP2350 USB (right-hand short edge)
part("J1", "TYPE-C-31-M-12", "USB_C", "USB_C_Receptacle_HRO_TYPE-C-31-M-12", "C165948", {
    "A4": "VBUS_NATIVE", "A9": "VBUS_NATIVE", "B4": "VBUS_NATIVE", "B9": "VBUS_NATIVE",
    "A1": GND, "A12": GND, "B1": GND, "B12": GND, "SH": GND,
    "A5": "CC1_NATIVE", "B5": "CC2_NATIVE",
    "A6": "USB_DP_CONN", "B6": "USB_DP_CONN", "A7": "USB_DM_CONN", "B7": "USB_DM_CONN",
    "A8": None, "B8": None,
})
# J2 = PIO USB on GP12/GP13 (bottom long edge, left)
part("J2", "TYPE-C-31-M-12", "USB_C", "USB_C_Receptacle_HRO_TYPE-C-31-M-12", "C165948", {
    "A4": "VBUS_PIO", "A9": "VBUS_PIO", "B4": "VBUS_PIO", "B9": "VBUS_PIO",
    "A1": GND, "A12": GND, "B1": GND, "B12": GND, "SH": GND,
    "A5": "CC1_PIO", "B5": "CC2_PIO",
    "A6": "PIO_DP_CONN", "B6": "PIO_DP_CONN", "A7": "PIO_DM_CONN", "B7": "PIO_DM_CONN",
    "A8": None, "B8": None,
})
# J3 = CH343P UART (bottom long edge, right)
part("J3", "TYPE-C-31-M-12", "USB_C", "USB_C_Receptacle_HRO_TYPE-C-31-M-12", "C165948", {
    "A4": "VBUS_UART", "A9": "VBUS_UART", "B4": "VBUS_UART", "B9": "VBUS_UART",
    "A1": GND, "A12": GND, "B1": GND, "B12": GND, "SH": GND,
    "A5": "CC1_UART", "B5": "CC2_UART",
    "A6": "UART_DP_CONN", "B6": "UART_DP_CONN", "A7": "UART_DM_CONN", "B7": "UART_DM_CONN",
    "A8": None, "B8": None,
})

# --- Pico-compatible 40 pin header and debug pads --------------------------
# The header is split into two 1x20 footprints.  This is both how a Pico
# header is normally fitted and how KiCad can keep the courtyard limited to
# the two pad rows instead of the whole area between them.
J5_NETS = {
    1: "UART0_TX", 2: "UART0_RX", 3: GND, 4: "GPIO2", 5: "GPIO3",
    6: "GPIO4", 7: "GPIO5", 8: GND, 9: "GPIO6", 10: "GPIO7",
    11: "GPIO8", 12: "GPIO9", 13: GND, 14: "GPIO10", 15: "GPIO11",
    16: "PIO_DP", 17: "PIO_DM", 18: GND, 19: "GPIO14", 20: "GPIO15",
    21: "GPIO16", 22: "GPIO17", 23: GND, 24: "GPIO18", 25: "GPIO19",
    26: "GPIO20", 27: "GPIO21", 28: GND, 29: "GPIO22", 30: "RUN",
    31: "GPIO26", 32: "GPIO27", 33: GND, 34: "GPIO28",
    35: "ADC_VREF", 36: P3V3, 37: "3V3_EN", 38: GND,
    39: VSYS, 40: "VBUS_NATIVE",
}
part("J5A", "PICO_2_HEADER_1", "PICO_HEADER_TOP", "PinHeader_1x20_Pico_Top", "",
     {str(n): J5_NETS[n] for n in range(1, 21)}, fitted=False)
part("J5B", "PICO_2_HEADER_2", "PICO_HEADER_BOTTOM", "PinHeader_1x20_Pico_Bottom", "",
     {str(n): J5_NETS[n] for n in range(21, 41)}, fitted=False)

part("J4", "DEBUG", "DEBUG", "PinHeader_1x03_P2.54mm_Vertical", "",
     {"1": "SWCLK", "2": GND, "3": "SWDIO"}, fitted=False)

# --- power OR and ESD ------------------------------------------------------
part("D1", "BAT54WS", "D", "D_SOD-323", "C22629", {"2": "VBUS_NATIVE", "1": VSYS})
part("D2", "BAT54WS", "D", "D_SOD-323", "C22629", {"2": "VBUS_PIO", "1": VSYS})
part("D3", "BAT54WS", "D", "D_SOD-323", "C22629", {"2": "VBUS_UART", "1": VSYS})

for ref, vbus, dp, dm in (
    ("D4", "VBUS_NATIVE", "USB_DP_CONN", "USB_DM_CONN"),
    ("D5", "VBUS_PIO", "PIO_DP_CONN", "PIO_DM_CONN"),
    ("D6", "VBUS_UART", "UART_DP_CONN", "UART_DM_CONN"),
):
    part(ref, "USBLC6-2SC6", "USBLC6", "SOT-23-6", "C7519", {
        "1": dp, "6": dp, "3": dm, "4": dm, "2": GND, "5": vbus,
    })

# --- CC resistors ----------------------------------------------------------
for ref, cc in (
    ("R1", "CC1_NATIVE"), ("R2", "CC2_NATIVE"),
    ("R3", "CC1_PIO"), ("R4", "CC2_PIO"),
    ("R5", "CC1_UART"), ("R6", "CC2_UART"),
):
    part(ref, "5.1k", "R", "R_0603_1608Metric", "C23186", {"1": cc, "2": GND})

# --- USB series resistors and PIO pull-up ----------------------------------
part("R7", "27", "R", "R_0603_1608Metric", "C25190", {"1": "USB_DP_CONN", "2": "USB_DP"})
part("R8", "27", "R", "R_0603_1608Metric", "C25190", {"1": "USB_DM_CONN", "2": "USB_DM"})
part("R9", "22", "R", "R_0603_1608Metric", "C23345", {"1": "PIO_DP_CONN", "2": "PIO_DP"})
part("R10", "22", "R", "R_0603_1608Metric", "C23345", {"1": "PIO_DM_CONN", "2": "PIO_DM"})
part("R11", "1.5k", "R", "R_0603_1608Metric", "C22843", {"1": "PIO_DP_CONN", "2": P3V3})

# --- boot / run / ADC / regulator ------------------------------------------
part("R12", "1k", "R", "R_0603_1608Metric", "C21190", {"1": "QSPI_SS", "2": "BOOT_SW"})
part("R13", "1k", "R", "R_0603_1608Metric", "C21190", {"1": "RUN", "2": "RUN_BTN"})
part("R14", "0", "R", "R_0603_1608Metric", "C21189", {"1": "QSPI_SS", "2": "FLASH_CS"})
part("R15", "33", "R", "R_0603_1608Metric", "C23140", {"1": P3V3, "2": "VREG_AVDD"})
part("R16", "200", "R", "R_0603_1608Metric", "C8218", {"1": P3V3, "2": "ADC_VREF"})
part("R17", "100k", "R", "R_0603_1608Metric", "C14675", {"1": VSYS, "2": "3V3_EN"})
part("R18", "1k", "R", "R_0603_1608Metric", "C21190", {"1": P3V3, "2": "PWR_LED_A"})
part("R19", "1k", "R", "R_0603_1608Metric", "C21190", {"1": P3V3, "2": "UART_LED_A"})

part("R20", "1k", "R", "R_0603_1608Metric", "C21190", {"1": "XOUT", "2": "XOUT_CRYSTAL"})
part("L1", "3.3uH", "L", "L_pol_2016", "C42411119", {"1": "VREG_LX", "2": P1V1})

# --- crystal ---------------------------------------------------------------
part("Y1", "ABM8-272-T3", "CRYSTAL", "Crystal_SMD_3225-4Pin_3.2x2.5mm", "C20625731", {
    "1": "XIN", "2": GND, "3": "XOUT_CRYSTAL", "4": GND,
})

# --- buttons ---------------------------------------------------------------
part("SW1", "BOOT", "SW", "SW_Push_1P1T_XKB_TS-1187A", "C318884",
     {"1": "BOOT_SW", "2": GND})
part("SW2", "RUN", "SW", "SW_Push_1P1T_XKB_TS-1187A", "C318884",
     {"1": "RUN_BTN", "2": GND})

# --- LEDs ------------------------------------------------------------------
part("LED1", "KT-0603R", "LED", "LED_0603_1608Metric", "C2286", {"2": "PWR_LED_A", "1": GND})
part("LED2", "KT-0603R", "LED", "LED_0603_1608Metric", "C2286", {"2": "UART_LED_A", "1": "UART_ACT"})

# --- decoupling ------------------------------------------------------------
def cap(ref, value, a, b, fp="C_0603_1608Metric", lcsc="C14663"):
    part(ref, value, "C", fp, lcsc, {"1": a, "2": b})

# local VBUS bulk and ESD decoupling, one set per port
for ref, vb in (("C1", "VBUS_NATIVE"), ("C2", "VBUS_PIO"), ("C3", "VBUS_UART")):
    cap(ref, "10uF", vb, GND, "C_0805_2012Metric", "C15850")
for ref, vb in (("C4", "VBUS_NATIVE"), ("C5", "VBUS_PIO"), ("C6", "VBUS_UART")):
    cap(ref, "100nF", vb, GND)

# regulator input / output
cap("C7", "10uF", VSYS, GND, "C_0805_2012Metric", "C15850")
cap("C8", "100nF", VSYS, GND)
cap("C9", "10uF", P3V3, GND, "C_0805_2012Metric", "C15850")
cap("C10", "100nF", P3V3, GND)

# RP2350 internal 1.1 V regulator
cap("C11", "4.7uF", P1V1, GND, "C_0805_2012Metric", "C1779")
cap("C12", "100nF", P1V1, GND)
cap("C13", "4.7uF", "VREG_AVDD", GND, "C_0805_2012Metric", "C1779")
cap("C14", "100nF", "VREG_AVDD", GND)

# IOVDD / QSPI / USB OTP / flash / CH343 / ADC decoupling
for i in range(15, 25):
    cap(f"C{i}", "100nF", P3V3, GND)
cap("C25", "15pF", "XIN", GND, lcsc="C1644")
cap("C26", "15pF", "XOUT_CRYSTAL", GND, lcsc="C1644")
cap("C27", "100nF", "V3_343", GND)
cap("C28", "100nF", "3V3_EN", GND)
cap("C29", "100nF", "ADC_VREF", GND)

PARTS = parts

# Nets used by the schematic generator
NETS = sorted({n for p in PARTS for n in p["pins"].values() if n})

# Power flags (net, reference)
POWER_FLAGS = [
    (GND, "#FLG01"),
    (VSYS, "#FLG02"),
    ("VBUS_NATIVE", "#FLG03"),
    ("VBUS_PIO", "#FLG04"),
    ("VBUS_UART", "#FLG05"),
    ("VREG_AVDD", "#FLG06"),
    ("ADC_VREF", "#FLG07"),
    ("3V3_EN", "#FLG08"),
    (P1V1, "#FLG09"),
]
