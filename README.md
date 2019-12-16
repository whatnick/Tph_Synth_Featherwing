# 3-Phase ELV synthesizer using DAC and Opamps

This is a FeatherWing ideally used with Teensy 3.2/4.0 to drive a high-speed DAC with 
filtering and signal conditioning using Opamps.

## Features :
- 50/60 Hz Frequency Selector ( Possibly just do it in software).
- Pot driven voltage Setting by controlling inverting-Opamp gain.
- Modified-Howland current source to simulate current clamp output.
- Pot driven current source using a tapped potentiometer attached to DAC output.
- ±5v RMS output using dual-rail Opamp mode - [OPA4170AIPW](https://au.element14.com/texas-instruments/opa4170aipw/op-amp-quad-rro-1mhz-14tssop/dp/2095843).
- Dual-voltage rail generation using [LM2663](https://au.element14.com/texas-instruments/lm2663mx-nopb/dc-dc-charge-pump-inverting-soic/dp/3008264) to flip 5v input to -5v.
- Boost-converter to push battery voltage (4.2v-3.7v) to 5v for non-USB power mode using [PAM2401](https://au.mouser.com/datasheet/2/115/PAM2401-347378.pdf).
- I2C DAC circuit to generate plausible phase shifted sine-wave, like in my [DIYODE 
Article](https://diyodemag.com/features/safe_3-phase_generator) using [MCP4728](https://au.element14.com/microchip/mcp4728-e-un/ic-dac-12bit-quad-10msop/dp/1800217).
- Fully open-source schematic/pcb in KiCAD.
![Schematic Screenshot](https://raw.githubusercontent.com/whatnick/Tph_Synth_Featherwing/master/doc/block_schematic.JPG)


## Roadmap Features :
- Experiment with power Opamps or eBay power amplifiers to output real 240v rail-to-rail swings.
- Experiment with power path IC's to manage supply from USB vs Battery. Particulary [LTC4412](https://www.analog.com/media/en/technical-documentation/data-sheets/4412fb.pdf) is of interest at high-power modes due to losses in [Schottky diodes](https://www.analog.com/media/en/technical-documentation/product-information/Battery_Management_Soulutions_PowerPath.pdf) and LV usage with buck-converters from 240v.
