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
