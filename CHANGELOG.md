# CHANGELOG

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