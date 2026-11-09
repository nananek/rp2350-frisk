"""Export the Specctra DSN used by Freerouting."""
import pcbnew

b = pcbnew.LoadBoard("pico2-compat.kicad_pcb")
if not pcbnew.ExportSpecctraDSN(b, "pico2.dsn"):
    raise SystemExit("ExportSpecctraDSN failed")
print("wrote pico2.dsn")
