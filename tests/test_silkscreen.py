import json
from pathlib import Path
import unittest

try:
    import pcbnew as pcb
except ImportError:
    pcb = None


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "Tph_Synth_Featherwing"


@unittest.skipIf(pcb is None, "Run with KiCad's bundled Python to validate PCB markings.")
class SilkscreenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.board = pcb.LoadBoard(str(PROJECT / "Tph_Synth_Featherwing.kicad_pcb"))

    def test_functional_labels_follow_actual_host_pads_on_both_sides(self):
        host = next(f for f in self.board.GetFootprints() if f.GetReference() == "MS1")
        labels = {
            "2": ("3V3", "+3V3"), "4": ("GND", "GND"),
            "17": ("SDA", "/DAC Based AC Generator/SDA"),
            "18": ("SCL", "/DAC Based AC Generator/SCL"),
            "26": ("VUSB", "/Boost_Converter/VUSB"),
            "28": ("VBAT", "/Boost_Converter/VBAT"),
        }
        self.assertTrue(set(labels).issubset({pad.GetNumber() for pad in host.Pads()}))
        for pad in host.Pads():
            if pad.GetNumber() not in labels:
                continue
            name, net = labels[pad.GetNumber()]
            self.assertEqual(pad.GetNetname(), net)
            for layer in (pcb.F_SilkS, pcb.B_SilkS):
                matches = [
                    text for text in self.board.GetDrawings()
                    if isinstance(text, pcb.PCB_TEXT) and text.GetText() == name
                    and text.GetLayer() == layer
                    and abs(text.GetPosition().x - pad.GetPosition().x) < pcb.FromMM(0.1)
                    and abs(text.GetPosition().y - pad.GetPosition().y) < pcb.FromMM(4)
                ]
                self.assertEqual(len(matches), 1, (name, layer))
                text = matches[0]
                self.assertEqual(text.IsMirrored(), layer == pcb.B_SilkS)
                self.assertAlmostEqual(pcb.ToMM(text.GetTextHeight()), 0.8)
                self.assertAlmostEqual(pcb.ToMM(text.GetTextThickness()), 0.2)

    def test_silk_checks_have_real_clearance_and_testpads_remain_identifiable(self):
        settings = json.loads((PROJECT / "Tph_Synth_Featherwing.kicad_pro").read_text(encoding="utf-8"))
        design = settings["board"]["design_settings"]
        self.assertGreaterEqual(design["rules"]["min_silk_clearance"], 0.15)
        for name in ("silk_overlap", "silk_over_copper", "silk_edge_clearance"):
            self.assertEqual(design["rule_severities"][name], "error")
        for footprint in self.board.GetFootprints():
            if footprint.GetReference().startswith("TP"):
                field = footprint.Reference()
                self.assertTrue(field.IsVisible(), footprint.GetReference())
                self.assertAlmostEqual(pcb.ToMM(field.GetTextHeight()), 0.8)
                self.assertAlmostEqual(pcb.ToMM(field.GetTextThickness()), 0.2)


if __name__ == "__main__":
    unittest.main()
