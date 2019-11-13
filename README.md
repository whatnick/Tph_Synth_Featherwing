# 3-Phase ELV synthesizer using DAC and Opamps

This is a FeatherWing ideally used with Teensy 3.2/4.0 to drive a high-speed DAC with 
filtering and signal conditioning using Opamps.

Roadmap Features :
- 50/60 Hz Frequency Selector ( Possibly just do it in software)
- Pot driven voltage Setting by controlling Opamp gain ( Again possibly just do it in 
software)
- ±12v RMS output ( requires Opamps capable of ±18V DC rails)
- Dual-voltage rail generation, [typical for 
synthesizers](https://www.allaboutcircuits.com/projects/build-your-own-negative-voltage-generator/)
- Boost-converter to push 5V to 18V rails
- I2C DAC circuit to generate plausible phase shifted sine-wave, like in my [DIYODE 
Article](https://diyodemag.com/features/safe_3-phase_generator)
