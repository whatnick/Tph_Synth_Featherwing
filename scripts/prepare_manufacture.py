"""Export a checked, traceable KiCad 10 fabrication and assembly-review package."""

import argparse
import collections
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
import zipfile


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "Tph_Synth_Featherwing"
STEM = "Tph_Synth_Featherwing"
BOM_FIELDS = (
    "References", "Quantity", "Value", "Footprint", "Manufacturer", "MPN",
    "DigiKey", "Mouser", "Assembly", "SourcingStatus", "SourcingNotes",
    "MouserOrderCode", "DigiKeyOrderCode", "DistributorChecked",
    "LCSCOrderCode",
)
SOURCE_FIELDS = BOM_FIELDS[4:]
FAB_EXTENSIONS = {".gtl", ".gbl", ".gts", ".gbs", ".gto", ".gbo", ".gtp", ".gbp", ".gm1", ".drl", ".gbrjob"}


def run(cli, *args):
    subprocess.run([str(cli), *map(str, args)], check=True)


def read_components(path):
    root = ET.parse(path).getroot()
    components = []
    for component in root.findall("components/comp"):
        fields = {v.attrib["name"]: v.text or "" for v in component.findall("fields/field")}
        properties = {v.attrib["name"] for v in component.findall("property")}
        components.append({
            "References": component.attrib["ref"],
            "Quantity": 1,
            "Value": component.findtext("value") or "",
            "Footprint": component.findtext("footprint") or "",
            **{name: fields.get(name, "") for name in SOURCE_FIELDS},
            "excluded": "exclude_from_bom" in properties or "dnp" in properties,
        })
    return components


def group_bom(components):
    groups = {}
    for component in components:
        if component["excluded"]:
            continue
        key = tuple(component[name] for name in BOM_FIELDS[2:])
        if key not in groups:
            groups[key] = {name: component[name] for name in BOM_FIELDS}
        else:
            groups[key]["Quantity"] += 1
            groups[key]["References"] += "," + component["References"]
    return sorted(groups.values(), key=lambda row: (row["Assembly"], row["MPN"], row["References"]))


def write_csv(path, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=BOM_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def assert_checks(erc, drc):
    issues = [v for sheet in erc["sheets"] for v in sheet["violations"]]
    issues += drc["violations"] + drc["unconnected_items"] + drc["schematic_parity"]
    if issues:
        raise ValueError(f"Manufacturing export blocked: {len(issues)} ERC/DRC/parity issues.")


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_hashes():
    paths = [PROJECT / (STEM + suffix) for suffix in (".kicad_pcb", ".kicad_pro")]
    paths += list(PROJECT.glob("*.kicad_sch"))
    paths += [PROJECT / "sym-lib-table", PROJECT / "fp-lib-table"]
    paths += list((PROJECT / "library").glob("*.kicad_sym"))
    paths += list((PROJECT / "footprints").rglob("*.kicad_mod"))
    paths += list((PROJECT / "3dmodels").iterdir())
    paths += [Path(__file__).resolve()]
    paths += list((ROOT / "sourcing").glob("distributor-review-*.json"))
    if (ROOT / "doc" / "pv36.pdf").is_file():
        paths.append(ROOT / "doc" / "pv36.pdf")
    return {str(path.relative_to(ROOT)): sha256(path) for path in sorted(paths) if path.is_file()}


def fabrication_archive(directory, destination):
    files = sorted(path for path in directory.iterdir() if path.suffix in FAB_EXTENSIONS)
    extensions = {path.suffix for path in files}
    if not FAB_EXTENSIONS.difference({".gbrjob"}).issubset(extensions):
        raise ValueError("Missing copper/mask/paste/silkscreen/outline/drill fabrication files.")
    if len([path for path in files if path.suffix == ".drl"]) != 2:
        raise ValueError("Expected separate PTH and NPTH drill files.")
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            if not path.stat().st_size:
                raise ValueError(f"Empty fabrication file: {path}")
            entry = zipfile.ZipInfo(path.name)
            entry.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(entry, path.read_bytes())
    with zipfile.ZipFile(destination) as archive:
        if archive.testzip() is not None or archive.namelist() != [p.name for p in files]:
            raise ValueError("Fabrication archive failed integrity validation.")
    return [path.name for path in files]


def board_info(board, pcb):
    edges = [item for item in board.GetDrawings() if item.GetLayer() == pcb.Edge_Cuts]
    if not edges:
        raise ValueError("Board outline is missing.")
    left = top = float("inf")
    right = bottom = float("-inf")
    for edge in edges:
        box = edge.GetBoundingBox()
        half_stroke = edge.GetWidth() / 2
        left = min(left, box.GetLeft() + half_stroke)
        right = max(right, box.GetRight() - half_stroke)
        top = min(top, box.GetTop() + half_stroke)
        bottom = max(bottom, box.GetBottom() - half_stroke)
    tracks = [t for t in board.GetTracks() if not isinstance(t, pcb.PCB_VIA)]
    vias = [t for t in board.GetTracks() if isinstance(t, pcb.PCB_VIA)]
    settings = json.loads((PROJECT / (STEM + ".kicad_pro")).read_text(encoding="utf-8"))
    return {
        "revision": board.GetTitleBlock().GetRevision(),
        "design_date": board.GetTitleBlock().GetDate(),
        "layers": board.GetCopperLayerCount(),
        "thickness_mm": pcb.ToMM(board.GetDesignSettings().GetBoardThickness()),
        "outline_width_mm": round(pcb.ToMM(right - left), 4),
        "outline_height_mm": round(pcb.ToMM(bottom - top), 4),
        "smallest_routed_track_mm": min(pcb.ToMM(t.GetWidth()) for t in tracks),
        "smallest_via_drill_mm": min(pcb.ToMM(t.GetDrillValue()) for t in vias),
        "smallest_via_diameter_mm": min(pcb.ToMM(t.GetFrontWidth()) for t in vias),
        "netclasses": [
            {name: netclass[name] for name in ("name", "clearance")}
            for netclass in settings["net_settings"]["classes"]
        ],
        "order_settings_to_confirm": {
            "material": "FR-4 proposed; confirm with fabricator",
            "copper_weight": "Not specified by design; confirm stackup and current/thermal suitability",
            "surface_finish": "Not specified by design; confirm finish and soldering process",
            "soldermask_colour": "Green proposed; cosmetic selection not encoded in design",
            "quantity": "Not specified; no order placed",
            "panelization": "Individual board; assembler must define panel rails/fiducials if required",
        },
    }


def prepare(cli, output):
    import pcbnew as pcb

    if output.exists() and any(output.iterdir()):
        raise ValueError(f"Output directory is not empty: {output}. Use a fresh directory to prevent stale files.")
    output.mkdir(parents=True, exist_ok=True)
    cli_version = subprocess.check_output([str(cli), "version"], text=True).strip()
    if not cli_version.startswith("10."):
        raise ValueError(f"Expected KiCad 10, got {cli_version}")
    inputs = source_hashes()
    reviews = sorted((ROOT / "sourcing").glob("distributor-review-*.json"))
    board_path = PROJECT / (STEM + ".kicad_pcb")
    schematic = PROJECT / (STEM + ".kicad_sch")
    board = pcb.LoadBoard(str(board_path))
    info = board_info(board, pcb)
    checks = output / "checks"
    fabrication = output / "fabrication"
    assembly = output / "assembly"
    for directory in (checks, fabrication, assembly):
        directory.mkdir()
    run(cli, "sch", "erc", schematic, "--severity-all", "--exit-code-violations",
        "--format", "json", "-o", checks / "erc.json")
    run(cli, "pcb", "drc", board_path, "--severity-all", "--schematic-parity",
        "--exit-code-violations", "--format", "json", "-o", checks / "drc.json")
    assert_checks(
        json.loads((checks / "erc.json").read_text(encoding="utf-8")),
        json.loads((checks / "drc.json").read_text(encoding="utf-8")),
    )
    run(cli, "sch", "export", "netlist", schematic, "--format", "kicadxml", "-o", checks / "netlist.xml")
    components = read_components(checks / "netlist.xml")
    physical = [c for c in components if not c["excluded"] and c["Assembly"] != "External host"]
    for component in [c for c in components if not c["excluded"]]:
        missing = [field for field in ("Manufacturer", "MPN", "DigiKey", "Mouser", "Assembly", "SourcingStatus") if not component[field]]
        if missing:
            raise ValueError(f"Missing sourcing fields on {component['References']}: {missing}")
    write_csv(assembly / "design-bom.csv", group_bom(components))
    write_csv(assembly / "assembly-bom-REVIEW-ONLY.csv", group_bom(physical))
    write_csv(assembly / "external-host.csv", group_bom([c for c in components if c["Assembly"] == "External host"]))
    for review in reviews:
        shutil.copyfile(review, assembly / review.name)
    run(cli, "pcb", "export", "pos", board_path, "--format", "csv", "--units", "mm",
        "--side", "both", "--smd-only", "--exclude-dnp", "-o", assembly / "positions-smt.csv")
    with (assembly / "positions-smt.csv").open(encoding="utf-8-sig", newline="") as stream:
        positions = list(csv.DictReader(stream))
    expected_smt = {c["References"] for c in physical if c["Assembly"] == "SMT"}
    if len(positions) != len(expected_smt) or {row["Ref"] for row in positions} != expected_smt:
        raise ValueError("SMT position file and assembly BOM do not match.")
    run(cli, "pcb", "export", "gerbers", board_path,
        "--layers", "F.Cu,B.Cu,F.Mask,B.Mask,F.Silkscreen,B.Silkscreen,F.Paste,B.Paste,Edge.Cuts",
        "--check-zones", "-o", fabrication)
    run(cli, "pcb", "export", "drill", board_path, "--format", "excellon",
        "--drill-origin", "absolute", "--excellon-units", "mm", "--excellon-separate-th",
        "--generate-map", "--map-format", "pdf", "--generate-report",
        "--report-path", checks / "drill-report.txt", "-o", fabrication)
    archive_name = f"{STEM}-v{info['revision']}-fabrication.zip"
    archive_members = fabrication_archive(fabrication, output / archive_name)
    run(cli, "sch", "export", "pdf", schematic, "-o", assembly / "schematic.pdf")
    with tempfile.TemporaryDirectory(prefix="tph-assembly-") as directory:
        drawing_board = pcb.LoadBoard(str(board_path))
        for footprint in drawing_board.GetFootprints():
            for field in footprint.GetFields():
                if field.GetName() != "Reference":
                    field.SetVisible(False)
            for graphic in footprint.GraphicalItems():
                if isinstance(graphic, pcb.PCB_TEXT):
                    graphic.SetVisible(False)
        drawing_path = Path(directory) / (STEM + ".kicad_pcb")
        pcb.SaveBoard(str(drawing_path), drawing_board)
        for side, layers in (("front", "F.Fab,F.Silkscreen,Edge.Cuts"), ("back", "B.Fab,B.Silkscreen,Edge.Cuts")):
            args = ["pcb", "export", "svg", drawing_path, "--layers", layers,
                    "--sketch-pads-on-fab-layers", "--page-size-mode", "2",
                    "--mode-single", "-o", assembly / f"assembly-{side}.svg"]
            if side == "back":
                args.append("--mirror")
            run(cli, *args)
    if inputs != source_hashes():
        raise ValueError("Design inputs changed during export; regenerate from a stable worktree.")
    blockers = [
        {
            "references": c["References"], "mpn": c["MPN"],
            "status": c["SourcingStatus"], "action": c["SourcingNotes"],
        }
        for c in physical if c["SourcingStatus"] != "VERIFIED_FOR_ORDER"
    ]
    summary = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "kicad_version": cli_version,
        "status": "FABRICATION_FILES_PREPARED_ASSEMBLY_ON_HOLD",
        "cad_checks": {"erc": 0, "drc": 0, "unconnected": 0, "schematic_parity": 0},
        "board": info,
        "physical_component_count": len(physical),
        "smt_placement_count": len(positions),
        "tht_references": [c["References"] for c in physical if c["Assembly"] == "THT"],
        "external_host_references": [c["References"] for c in components if c["Assembly"] == "External host"],
        "pcb_feature_references": [c["References"] for c in components if c["excluded"]],
        "feather_header_assembly_policy": {
            "factory_population": "DNP",
            "purchasing_bom": "Excluded; no factory header MPN required.",
            "user_installation": "Fit compatible Feather stacking headers after manufacture as required.",
            "scope": "Feather host 12-pin/16-pin rows only; J2 and J3 remain fitted BOM components.",
        },
        "procurement_blockers": blockers,
        "live_distributor_stock_pricing_packaging": (
            "See dated distributor-review JSON in assembly; observations are not purchasing approval."
            if reviews else "NOT_VERIFIED"
        ),
        "additional_release_actions": [
            "Validate approved capacitor replacements under operating bias/temperature, including boost and charge-pump stability and analog compensation.",
            "PV36W pitch/pin mapping verified: check R10 0.8mm drills versus recommended 0.9mm and exact body/tool clearance; proxy STEP is not certification.",
            "Check panel-pot physical seating: aligned family STEP lead sections fit at board midplane but small mounting-feature/board intersections remain.",
            "Confirm material, copper weight, finish, quantity and panelization with fabricator/assembler.",
            "Have assembler confirm SMT rotations, polarity, tooling and the absolute-origin position-file convention.",
            "Bench-test power rails, I2C/DAC, analog outputs and Howland current source before production.",
        ],
        "coordinate_convention": "Absolute CAD origin for Gerber/drill/positions; mm; KiCad Cartesian position CSV; bottom X not negated. Back assembly drawing is mirrored for viewing.",
        "fabrication_archive": {"filename": archive_name, "members": archive_members},
    }
    (output / "release-status.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (output / "README.txt").write_text(
        f"3-Phase Synth FeatherWing v{info['revision']} manufacturing preparation\n\n"
        "STATUS: Fabrication files prepared; ASSEMBLY/PURCHASING ON HOLD.\n"
        "This is not approval to manufacture or order components.\n"
        f"Nominal outline: {info['outline_width_mm']} x {info['outline_height_mm']} mm; "
        f"{info['layers']} copper layers; {info['thickness_mm']} mm board.\n"
        "Confirm FR-4, copper weight, finish, quantity and panelization before an order.\n\n"
        f"Bare-board archive: {archive_name}\n"
        "Contains fresh Gerbers and separate PTH/NPTH drills only (plus job file if emitted).\n"
        "Drill maps and checks remain outside the upload archive.\n"
        "Do not use the historical Tph_Synth_Featherwing\\gerbers or bom folders.\n\n"
        "assembly\\assembly-bom-REVIEW-ONLY.csv is NOT an approved purchasing BOM.\n"
        "C1-C3, C4-C11/C18 and C12 use approved breakout replacements; hardware validation remains required.\n"
        "R10 needs exact mechanical/pin verification. Feather host headers are intentionally DNP, not a factory release blocker.\n"
        "See assembly\\distributor-review-*.json for dated MCP stock, lifecycle and packaging evidence.\n"
        "TDK 22uF replacements are sourced through LCSC/JLCPCB; verify exact MPN supply before ordering.\n"
        "All legacy MPNs still require electrical/mechanical qualification and a fresh stock check before ordering.\n"
        "MS1 is the external host; no adapter PCB is fitted to this PCB at MS1.\n"
        "DO NOT FIT Feather host 12-pin/16-pin headers at manufacture; excluded from purchasing BOM.\n"
        "Users fit compatible stacking headers to suit their Feather after manufacture. J2/J3 remain fitted.\n"
        "JP1/JP2, test pads and the OSHW logo are PCB features, not purchased components.\n\n"
        "positions-smt.csv covers SMT only; THT parts are listed in release-status.json.\n"
        "Gerbers/drills/positions use absolute CAD origin, millimetres; bottom X is not negated.\n"
        "Back assembly SVG is mirrored for viewing only. Confirm machine rotations and polarity.\n"
        "Unvalidated hardware: power rails, host I2C/firmware, DAC and analog/current outputs.\n"
        "See release-status.json for blockers and manifest.json for source/output SHA-256 hashes.\n",
        encoding="utf-8",
    )
    manifest = {
        "inputs_sha256": inputs,
        "outputs_sha256": {
            str(path.relative_to(output)): sha256(path)
            for path in sorted(output.rglob("*")) if path.is_file()
        },
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {output}; {len(physical)} fitted parts, {len(positions)} SMT positions.")
    print("ASSEMBLY/PURCHASING ON HOLD: see release-status.json and dated sourcing evidence; no order approval.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cli", type=Path, help="KiCad 10 kicad-cli.exe path")
    parser.add_argument("--output", type=Path, required=True, help="New or empty destination directory")
    args = parser.parse_args()
    cli = args.cli or Path(sys.executable).with_name("kicad-cli.exe")
    if not cli.is_file():
        found = shutil.which("kicad-cli")
        if not found:
            parser.error("KiCad CLI not found; supply --cli.")
        cli = Path(found)
    prepare(cli, args.output.resolve())


if __name__ == "__main__":
    main()
