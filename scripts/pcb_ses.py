"""Import the Freerouting SES session into the KiCad board."""
import pcbnew

b = pcbnew.LoadBoard("pico2-compat.kicad_pcb")
if not pcbnew.ImportSpecctraSES(b, "pico2.ses"):
    raise SystemExit("ImportSpecctraSES failed")
pcbnew.SaveBoard("pico2-compat.kicad_pcb", b)
print("imported pico2.ses")
