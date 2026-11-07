import importlib.util
from pathlib import Path
import tempfile
import unittest
import zipfile


SPEC = importlib.util.spec_from_file_location(
    "prepare_manufacture", Path(__file__).resolve().parents[1] / "scripts" / "prepare_manufacture.py"
)
mfg = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mfg)


class ManufacturingTests(unittest.TestCase):
    def component(self, ref, **overrides):
        return {
            **{name: "" for name in mfg.BOM_FIELDS},
            "References": ref, "Quantity": 1, "Value": "10k",
            "Footprint": "Resistor_SMD:R_0603_1608Metric",
            "Manufacturer": "YAGEO", "MPN": "RT0603FRD0710KL",
            "Assembly": "SMT", "excluded": False, **overrides,
        }

    def test_bom_excludes_virtuals_and_keeps_package_and_review_groups_distinct(self):
        rows = mfg.group_bom([
            self.component("R1"), self.component("R4"),
            self.component("TP1", excluded=True),
            self.component("R5", Footprint="Resistor_SMD:R_0402_1005Metric"),
            self.component("R6", SourcingStatus="HOLD_PACKAGE_MISMATCH"),
        ])
        self.assertEqual(len(rows), 3)
        self.assertEqual(sum(row["Quantity"] for row in rows), 4)
        self.assertEqual(next(row["Quantity"] for row in rows if row["References"] == "R1,R4"), 2)

    def test_reader_preserves_sourcing_and_external_host_but_excludes_bom_features(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "net.xml"
            path.write_text(
                '<export><components><comp ref="MS1"><value>Adapter</value>'
                '<fields><field name="MPN">3200</field><field name="Assembly">External host</field></fields>'
                '</comp><comp ref="JP1"><property name="exclude_from_bom"/></comp>'
                '<comp ref="R1"><property name="dnp"/></comp>'
                '<comp ref="U3"><fields><field name="MouserOrderCode">595-LM324PWR</field>'
                '<field name="DistributorChecked">2026-11-07</field>'
                '<field name="SourcingStatus">REVIEW_DATASHEET_AND_FIT</field>'
                '</fields></comp><comp ref="C1"><fields>'
                '<field name="MPN">C2012X5R1V226MT000E</field>'
                '<field name="LCSCOrderCode">C338080</field>'
                '<field name="SourcingStatus">APPROVED_FOR_BREAKOUT_PENDING_VALIDATION</field>'
                '</fields></comp></components></export>',
                encoding="utf-8",
            )
            rows = mfg.read_components(path)
            self.assertEqual(rows[0]["Assembly"], "External host")
            self.assertEqual(rows[0]["MPN"], "3200")
            self.assertTrue(rows[1]["excluded"])
            self.assertTrue(rows[2]["excluded"])
            self.assertEqual(rows[3]["MouserOrderCode"], "595-LM324PWR")
            self.assertEqual(rows[3]["DistributorChecked"], "2026-11-07")
            self.assertEqual(rows[3]["SourcingStatus"], "REVIEW_DATASHEET_AND_FIT")
            self.assertEqual(rows[4]["LCSCOrderCode"], "C338080")
            self.assertEqual(rows[4]["SourcingStatus"], "APPROVED_FOR_BREAKOUT_PENDING_VALIDATION")

    def test_even_warning_or_parity_only_findings_block_exports(self):
        erc = {"sheets": [{"violations": []}]}
        drc = {"violations": [], "unconnected_items": [], "schematic_parity": [{"severity": "warning"}]}
        with self.assertRaises(ValueError):
            mfg.assert_checks(erc, drc)
        drc["schematic_parity"] = []
        mfg.assert_checks(erc, drc)

    def test_archive_has_only_current_fabrication_files_and_split_drills(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fab = root / "fab"
            fab.mkdir()
            for suffix in mfg.FAB_EXTENSIONS - {".gbrjob"}:
                (fab / ("board" + suffix)).write_text("fabrication", encoding="ascii")
            (fab / "board-NPTH.drl").write_text("drill", encoding="ascii")
            (fab / "board-map.pdf").write_bytes(b"map")
            (fab / "legacy.zip").write_bytes(b"stale")
            destination = root / "upload.zip"
            names = mfg.fabrication_archive(fab, destination)
            self.assertNotIn("board-map.pdf", names)
            self.assertNotIn("legacy.zip", names)
            with zipfile.ZipFile(destination) as archive:
                self.assertIsNone(archive.testzip())
            (fab / "board-NPTH.drl").unlink()
            with self.assertRaises(ValueError):
                mfg.fabrication_archive(fab, destination)


if __name__ == "__main__":
    unittest.main()
