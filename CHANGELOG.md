# CHANGELOG

## Potentiometer mechanical review (2026-11-07)
- Verify PV36W inline pitch and pin order from supplied doc/pv36.pdf.
  Flag 0.8 mm PCB drills versus 0.9 mm manufacturer recommendation.
- Correct four panel-pot family STEP X offsets 3.5 to 3.1 mm and matching
  project-local footprint offset without changing pads/routing/placement.
- Measure all 20 modeled lead/tab sections through the board; document
  residual mounting-feature intersections and unavailable exact PV36W model.
- Add populated-STEP Blender turntable (doc/v0.4/board-turntable.mp4) and
  scripts/render_turntable.py; refresh top/bottom renders.

## Feather header assembly policy (2026-11-07)
- Leave Feather host 12-pin/16-pin headers DNP at manufacture, excluding them
  from factory purchasing; users fit stacking headers as required afterward.
- Remove factory header selection from manufacturing blockers. J2/J3 remain
  fitted. R10 PV36W-to-3296W fit remains unverified, not a confirmed mismatch.

## Approved breakout capacitor substitutions (2026-11-07)
- Apply user-approved TDK C2012X5R1V226MT000E (22 uF, 35 V, 0805) at C1-C3,
  Murata GRM21BR61H106KE43L (10 uF, 50 V, 0805) at C4-C11/C18, and YAGEO
  CC0603BRNPO9BN5R0 (5 pF, 50 V, 0603) at C12.
- Preserve capacitance, footprint, component placement and routing; no voltage
  rating reduced. Synchronize standard MPN and legacy manf# fields.
- Record LCSC sourcing for TDK, exact distributor codes and approved-breakout
  status. Production release still requires DC-bias, stability and hardware
  validation, R10 fit and header/stacking decisions.

## Live distributor sourcing review (2026-11-07)
- Use the connected pcbparts MCP for all 21 unique fitted MPNs in Mouser
  batches and targeted DigiKey checks. Record dated evidence and exact
  manufacturer/order-code fields on all 46 fitted schematic/PCB components.
- Confirm C1-C3 obsolete at both distributors and flag C4-C11/C18 zero stock
  at both. Keep C12's package and R10's mechanical holds; no MPNs substituted.
- Record active YAGEO C12 qualification candidate and reject the earlier
  NRND Murata candidate. Exclude unrelated same-MPN manufacturer matches.
- Regenerate the source-derived review BOM and manufacturing package with
  dated evidence and source/output hashes; assembly/purchasing remains on hold.

## Manufacturing preparation and issue #3 (2026-11-06)
- Add aligned SDA, SCL, 3V3, GND, VUSB and VBAT labels at their actual Feather
  header pads on both silkscreen layers, mirrored correctly on the back.
- Enforce 0.15 mm silkscreen clearance instead of the former zero-clearance
  threshold. Remove the eight exposed overlaps, retain visible test-pad
  references and move U4's reference clear of the new 3V3 marking.
- Preserve all routed copper, pad geometry and component placement.
- Add schematic/PCB sourcing fields and a reproducible manufacturing exporter
  with checked Gerbers, split drills, review BOM, SMT placements and hash manifest.
- Keep assembly/purchasing on hold for the documented C12 package mismatch,
  C1-C3 lifecycle review, R10 fit, header selection and remaining sourcing checks.

## v0.4 - KiCad 10 migration (2026-10-28)
- Upgrade the six-sheet schematic, PCB and project-local libraries to KiCad 10.
- Restore hierarchical instances, annotate the remaining power symbol and
  retain the correct unit selection when opening the op-amp sheet standalone.
- Synchronize all PCB pad nets, schematic paths, component fields and BOM
  exclusions without changing the existing routed copper topology.
- Update PCB silkscreen and schematic/PCB title blocks to revision 0.4.
- Add project-local edge-mounted footprint variants: keep silkscreen inside
  the PCB while retaining off-board mechanical graphics on the fabrication layer.
  Silkscreen-edge checking is enabled, not suppressed.
- Restore the existing project-local connector, potentiometer and inductor
  STEP models with their original placement transforms.
- Correct sheet numbering and improve crowded schematic reference/value fields.
- Validate with KiCad 10 ERC and DRC including schematic parity: zero violations,
  zero unconnected items and zero parity mismatches. Verify PDF, netlist,
  Gerber, drill and assembled STEP exports and inspect schematic/PCB renders.
- Retain the migration's 0.15 mm Default/Power netclass clearances. This is a CAD
  compatibility revision; analog performance and host firmware still require
  hardware validation.

## Initial Part Selection (2019-11-13)
- DAC - 
[MCP4728](https://au.element14.com/microchip/mcp4728-e-un/ic-dac-12bit-quad-10msop/dp/1800217)
- Quad Opamp - 
[OPA4170AIPW](https://au.element14.com/texas-instruments/opa4170aipw/op-amp-quad-rro-1mhz-14tssop/dp/2095843)
- Negative Rail Generator - 
[LM2663](https://au.element14.com/texas-instruments/lm2663mx-nopb/dc-dc-charge-pump-inverting-soic/dp/3008264)

## Battery to 5V boost converter (2019-12-16)
- Added boost converter -
[PAM2401](https://au.mouser.com/datasheet/2/115/PAM2401-347378.pdf)

## AC Constant Current source (2019-12-17)
- Uses spare opamp of Quad-opamp package in [modified-Howland current pump](http://www.ti.com/lit/an/snoa474a/snoa474a.pdf) mode.

## Perform parts search and footprint assignment (2019-12-17)
- Use 3A Schottky diodes [B330B-13-F](https://au.mouser.com/ProductDetail/Diodes-Incorporated/B330B-13-F?qs=cOsaT%252BRvuElEdEmWP6m3Zg%3D%3D) in SMB package.
- Use 2.2uH fixed inductor for Murata [LQH44PH2R2MPRL](https://au.mouser.com/ProductDetail/Murata-Electronics/LQH44PH2R2MPRL?qs=sGAEpiMZZMsg%252By3WlYCkU6W%2FGUkfqxhZhlKFJeq0hl8%3D) or Bourns [SRN5020TA-2R2M](https://au.mouser.com/ProductDetail/Bourns/SRN5020TA-2R2M?qs=sGAEpiMZZMsg%252By3WlYCkUwWVs%252BZAfRN3wkg12PxQP2E%3D)
- The Howland current pump needs a trim pot, use an SMD version [PVG5A202C03R00](https://au.mouser.com/ProductDetail/Bourns/PVG5A202C03R00?qs=sGAEpiMZZMvygUB3GLcD7qR9snKKmVdvJfukCFXNzPo%3D) or cheapest THT version [PV36W202C01B00](https://au.mouser.com/ProductDetail/Bourns/PV36W202C01B00?qs=sGAEpiMZZMvygUB3GLcD7u3z%252BNHL9M9LPXQekd6c8ZA%3D)
- Use linear rotaty pots for gain control pending feedback - [PTV09A-2020F-B104](https://au.mouser.com/ProductDetail/Bourns/PTV09A-2020F-B104?qs=sGAEpiMZZMtC25l1F4XBU1xwXnrUt%2FuomuwWp9Hu9qc%3D)

## Update L for 3A (2019-12-19)
- Initial choice had 3A as saturation current instead of operating current [SRR1005-2R2M](https://www.digikey.com/product-detail/en/bourns-inc/SRR1005-2R2M/SRR1005-2R2MTRTR-ND/419242).
- Perform initial placement. Group functional blocks together and add missing 3D parts from manufacturer in the 3dmodels directory.
- Do a prelim auto-route to spot placment errors and check routing feasibility.