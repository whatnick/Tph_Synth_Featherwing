# 3-Phase ELV synthesizer using DAC and Opamps

This is a FeatherWing ideally used with Teensy 3.2/4.0 to drive a high-speed DAC with 
filtering and signal conditioning using Opamps.

## KiCad 10 design

Revision **v0.4 (2026-10-28)** is maintained in
`Tph_Synth_Featherwing\Tph_Synth_Featherwing.kicad_pro`. Open that project and
its root schematic rather than treating the hierarchical sheets as separate
projects. The revision is also printed on the PCB bottom silkscreen.

The project-local symbol and footprint tables resolve the converted libraries,
board-edge silkscreen variants and existing `3dmodels` assets. Keep these
directories together with the project and install the standard KiCad 10
symbol, footprint and 3D-model libraries.

From the repository root, validate with KiCad 10's `kicad-cli` on `PATH`:

```powershell
kicad-cli sch erc .\Tph_Synth_Featherwing\Tph_Synth_Featherwing.kicad_sch --severity-all --exit-code-violations
kicad-cli pcb drc .\Tph_Synth_Featherwing\Tph_Synth_Featherwing.kicad_pcb --severity-all --schematic-parity --exit-code-violations
```

Both checks pass with zero violations, unconnected items or schematic-parity
mismatches. All 515 existing tracks/vias and component placement are preserved.
The Default and Power netclasses use 0.15 mm clearance; silkscreen-edge checking
is enabled. See [the v0.4 schematic](doc/v0.4/schematic.pdf) and
[top](doc/v0.4/board-top.png)/[bottom](doc/v0.4/board-bottom.png) renders.
These CAD checks do not replace hardware/firmware and analog-output testing.

## Manufacturing preparation

The current preparation is in `manufacturing\v0.4`. **Assembly and purchasing
are on hold**, even though the CAD checks pass. Use the freshly generated
fabrication ZIP there, not the historical `Tph_Synth_Featherwing\gerbers`,
`bom` spreadsheet or iBOM. The archive has copper, mask, silkscreen, paste and
outline Gerbers plus separate PTH/NPTH drills. The nominal outline is
51 x 58.5 mm, two copper layers, 1.6 mm board thickness. Confirm material,
copper weight, surface finish, quantity and panelization with the fabricator;
none has been ordered.

Generate a new package into an empty directory using KiCad's bundled Python:

```powershell
& 'C:\Program Files\KiCad\10.0\bin\python.exe' .\scripts\prepare_manufacture.py --output .\manufacturing\v0.4-new
```

The exporter requires zero ERC, DRC, unconnected and parity findings. It derives
the BOM from schematic fields, checks SMT placements against that BOM and
records input/output SHA-256 hashes in `manifest.json`. Regenerate into a new
directory if the destination is already populated; it deliberately refuses to
mix old and new exports. `release-status.json` records every sourcing review
and release action. Positions are in millimetres using the absolute CAD origin
for Gerbers, drills and placements; bottom X is not negated. Have the assembler
verify rotations, polarity and panel tooling. THT parts are listed separately
from the SMT position file.

For [issue #3](https://github.com/whatnick/Tph_Synth_Featherwing/issues/3),
SDA, SCL, 3V3, GND, VUSB and VBAT are labelled at the Feather header pads on
both PCB sides. Back-side labels are mirrored for correct fabrication.
Silkscreen checks enforce 0.15 mm clearance; test-pad references and the U4
reference are positioned clear of other markings. Run the tests with KiCad's
bundled Python to include the PCB pin-label and silkscreen-rule checks:

```powershell
& 'C:\Program Files\KiCad\10.0\bin\python.exe' -m unittest discover -s tests -v
```

Known release blockers:

- **C12:** `GJM0335C1E5R0BB01D` is 0201 imperial (0603 metric), but the board
  footprint is 0603 imperial (1608 metric). The legacy MPN is retained and
  flagged, not silently substituted. Select a verified 5 pF C0G part matching
  the required tolerance and footprint before ordering.
- **C1-C3:** distributor search results flag `C2012JB1V226M125AC` as obsolete.
  Confirm lifecycle and qualify an 0805 22 uF replacement, including voltage
  rating, DC bias and converter stability.
- **R10:** verify `PV36W202C01B00` body/lead geometry, pin numbering and adjustment
  access against the Bourns 3296W footprint.
- **Host interface:** Adafruit
  [3200](https://www.adafruit.com/product/3200) is an external Teensy-to-Feather
  adapter, not a component fitted at MS1. It is listed separately from the PCB
  assembly BOM. Select mating 12-pin/16-pin headers and stacking height;
  headers and the Teensy are not selected assembly line items.
- All other legacy MPNs still require datasheet, stock, packaging, price and
  lifecycle verification. Bench-test power rails, I2C/DAC, analog outputs and
  the Howland current source before a production release.

`Manufacturer`, `MPN`, `Description`, `DigiKey`, `Mouser`, `Assembly`,
`SourcingStatus` and `SourcingNotes` live on the schematic symbols and are
mirrored to the PCB for parity. Distributor fields are **search URLs**, not
verified order codes or availability claims. This package does not use a
distributor API or claim live availability. In Copilot CLI, `/mcp` manages
additional MCP connections; an approved read-only integration could use the official
[DigiKey developer API](https://developer.digikey.com/) and
[Mouser Search API](https://www.mouser.com/api-search/). Keep API credentials
outside the repository; no server or credential configuration is changed here.

## Features :
- 50/60 Hz Frequency Selector ( Possibly just do it in software).
- Pot driven voltage Setting by controlling inverting-Opamp gain.
- Modified-Howland current source to simulate current clamp output.
- Pot driven current source using a tapped potentiometer attached to DAC output.
- ±5v RMS output using dual-rail Opamp mode - [OPA4170AIPW](https://au.element14.com/texas-instruments/opa4170aipw/op-amp-quad-rro-1mhz-14tssop/dp/2095843) or [LM324PWR](https://au.element14.com/texas-instruments/lm324pwr/ic-op-amp-1-2mhz-0-5v-us-tssop/dp/2342289)
- Dual-voltage rail generation using [LM2663](https://au.element14.com/texas-instruments/lm2663mx-nopb/dc-dc-charge-pump-inverting-soic/dp/3008264) to flip 5v input to -5v.
- Boost-converter to push battery voltage (4.2v-3.7v) to 5v for non-USB power mode using [PAM2401](https://au.mouser.com/datasheet/2/115/PAM2401-347378.pdf).
- I2C DAC circuit to generate plausible phase shifted sine-wave, like in my [DIYODE 
Article](https://diyodemag.com/features/safe_3-phase_generator) using [MCP4728](https://au.element14.com/microchip/mcp4728-e-un/ic-dac-12bit-quad-10msop/dp/1800217).
- Fully open-source schematic/pcb in KiCAD.
![Schematic Screenshot](https://raw.githubusercontent.com/whatnick/Tph_Synth_Featherwing/master/doc/block_schematic.JPG)


## Roadmap Features :
- Experiment with power Opamps or eBay power amplifiers to output real 240v rail-to-rail swings.
- Experiment with power path IC's to manage supply from USB vs Battery. Particulary [LTC4412](https://www.analog.com/media/en/technical-documentation/data-sheets/4412fb.pdf) is of interest at high-power modes due to losses in [Schottky diodes](https://www.analog.com/media/en/technical-documentation/product-information/Battery_Management_Soulutions_PowerPath.pdf) and LV usage with buck-converters from 240v.
- Add I2C digital pots instead of physical pots.
