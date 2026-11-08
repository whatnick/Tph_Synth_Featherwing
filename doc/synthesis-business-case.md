# ELV synthesis: market, lab TCO and NILM replay assessment

Assessment date: 2026-11-08. This is a decision-support assessment, not a sales
forecast, final supplier quotation, hardware qualification or implemented NILM
system. Prices retain the source currency; tax, shipping and configuration can
change. Cost scenarios below are explicitly assumptions.

## Recommendation

Retain v0.4 as a small-batch ELV teaching, experimentation and metering-front-end
test platform. There is a plausible niche, but **no demonstrated volume business
case**: no sales history, conversion rate, customer interviews or procurement
commitments were available for this assessment. The existing Tindie price is
US$50 and the listing is out of stock [1]. At that price, test/support costs can
consume the margin.

Do not commission a larger production run on the strength of competitor prices.
First complete the ten-board RFQ, fit and bench checks, then seek paid interest
from educators and energy-monitor developers. Test US$69-79 as a proposed
board-only price, not an approved price change. A documented lab kit, repeatable
firmware and paid integration work are more defensible than an undifferentiated
DAC breakout. Keep inventory small; use common parts and build against demand.

For NILM, start with software-generated/recorded signatures and a single-phase
ELV replay experiment. A six-channel, synchronous, higher-bandwidth successor is
a separate R&D decision, not a capability of this board. Pretraining is feasible
in principle; real-household generalization must be measured, not inferred from
success on a synthetic bench.

## What this board actually provides

The root KiCad schematic exposes `VA_out`, `VB_out`, `VC_out` and `IAC_out`.
There is one four-channel MCP4728 I2C DAC and a Howland current-output stage:
**3V + 1I, not independent 3V + 3I**. Three-phase voltage demonstration and
one phase's current/power-factor experiments are useful initial targets.
Arbitrary independent loads on all three phases require additional current
channels and synchronous generation.

The public listing describes a historical 9 V peak-to-peak prototype [1].
That would be about 3.18 V RMS for a sine wave; it is not a current-v0.4 accuracy
or loaded-output guarantee. Nominal +/-5 V supply rails do not imply +/-5 V RMS
output. The 2017 blog shows the original Teensy/MCP4728 prototype and scope
testing [2], not release qualification for this revision.

The MCP4728 has four 12-bit buffered outputs and a typical 6 us settling time
[3]. Settling time is not the sustained four-channel waveform sample rate.
As an illustrative I2C limit, an address plus eight data bytes with ACK bits
takes approximately 81 clock periods: at an assumed 400 kHz bus, that is at most
4.94 k four-channel transfers/s before firmware and bus overhead. That is about
99 vectors per 50 Hz cycle, with an ideal Nyquist limit of 2.47 kHz before the
analog filters. This is an upper-bound calculation, not a measured rate or a
claim of simultaneous output latching. Measure channel skew, jitter and
frequency response on the actual host. Do not advertise faithful replay of
30 kHz or 44.1 kHz datasets from this estimate.

Use only a disconnected, verified ELV test fixture with suitable signal limits.
This is signal-level stimulus, not a power source for real appliances, CT
primary excitation, a certified calibrator or permission to connect to a
mains-referenced meter. Injection after a transducer omits that transducer's
transfer function. Keep that limitation in every experiment's metadata.

## Similar equipment and verified price observations

Only prices actually read from the product pages/listing are treated as observed.
Generic search estimates for professional calibrators were not adopted.

| Alternative | Observed price | Relevant capability and limitation |
| --- | --- | --- |
| This FeatherWing on Tindie [1] | US$50, out of stock | Historical 3-phase ELV product; host required; v0.4 qualification pending. |
| Adafruit MCP4728 breakout [3] | US$7.50; US$6.75 at 10-99 | Four unipolar voltage DAC outputs, I2C; host, bipolar conditioning, current stage and fixtures extra. Strong low-cost DIY substitute, not an equivalent finished rig. |
| Digilent Analog Discovery 3 [4] | A$620 displayed | Two +/-5 V, 14-bit, up-to-125 MS/s AWG outputs, plus two scope channels and SDK. Excellent single-phase V/I tool; not three independent phase voltages. |
| Eclypse Z7 + two Zmod AWG 1411 modules [5,6] | A$875 + 2 x A$175 = A$1,225 | Four single-ended, 14-bit, up-to-100 MS/s voltage outputs. Cross-module synchronization requires an implemented and validated FPGA design; current conversion, acquisition and fixtures extra. Still not six V/I channels. |
| Typhoon HIL404 [7] | Quote required | 16 analog inputs and 16 analog outputs, 16-bit, +/-10 V signal I/O and real-time models; much broader signal-HIL platform, not a stand-alone power source. |
| Chroma 63800 AC load [8] | Quote required | 1.8-4.5 kW models, 50-350 V RMS, controllable PF/crest factor, rectifier/inrush load modes. Practical power-load emulation, but outside this ELV board's scope and not arbitrary signature replay by default. |

Do not confuse oscilloscope input count with generator output count. Combining
two cheap dual-channel generators does not establish cross-unit phase coherence.
Likewise, a four-output generator cannot provide six independent V/I signals.
A generic audio interface can be a replay research component, but AC coupling,
common grounds, output scaling and synchronization need qualification.

The likely differentiation is a compact, documented and tested **ELV learning
fixture**, not high-speed synthesis or metrology-grade accuracy. Professional
power standards and power-HIL systems address different requirements; their
quotation-only prices do not prove willingness to pay for this product.

## Board economics and demand gates

The submitted ten-board Elecrow request remains Pending Quotation. It shows
US$10 PCB + US$12 stencil + US$66 assembly = US$88, with US$15.94 freight
separate. **US$0 components means not priced**, not free. Its overhead is
US$10.394 per board if all ten are usable. Uploaded BOM and placement hashes
are retained in the manufacturing request record.

Matching the fitted review BOM against the dated distributor evidence and
approved substitution records gives a known component subtotal of
**US$21.7579 per board, excluding nine GRM21BR61H106KE43L capacitors**.
This mixes dated single-unit distributor observations with the recorded TDK
candidate price, not Elecrow purchasing prices or a bulk-reel quote. Thus
US$32.1519 (known components + RFQ overhead) is an incomplete arithmetic
baseline, not a landed cost. Still missing are those capacitors, sourcing
charges, surplus/MOQs, import costs, yield losses, test labour and packing.

For decision sensitivity only, assume variable cost `C` of US$35 (optimistic)
or US$45 per saleable board, inclusive of production/test/packing/returns
allowance. Assume channel/payment costs of 10% of sale price, not a claim about
Tindie's actual fee schedule, and incremental validation/documentation cost
`F = US$3,000` (30 hours at a hypothetical US$100/h).

`contribution = 0.90 * price - C`

`break-even boards = ceil(F / contribution)`, only when contribution is positive.

| Proposed sale price | Contribution at C=35 | Break-even | Contribution at C=45 | Break-even |
| --- | ---: | ---: | ---: | ---: |
| US$50, current listing | US$10.00 | 300 boards | US$0.00 | No recovery of fixed cost |
| US$69 | US$27.10 | 111 boards | US$17.10 | 176 boards |
| US$79 | US$36.10 | 84 boards | US$26.10 | 115 boards |

These are contribution margins, not profits; advertising, further R&D, business
overheads and tax are not included. If manual support takes 15 minutes per sale
at that hypothetical US$100/h, it consumes another US$25 unless already
covered in `C`. A small run can be useful internally without recovering
commercial development cost.

Suggested gates, not measured demand: qualify the first articles; demonstrate
useful host firmware and at least three reproducible lab exercises; obtain
five paid reservations or two institutional pilot commitments before another
batch; replace assumed `C` with the final quote and timed production test.
Do not change the listing price, stock status or release claims before approval.
If these gates fail, keep the board as lab infrastructure and portfolio/contract
lead generation rather than stocking a speculative retail line.

## Three-year lab TCO even if retail demand is weak

Compare purchases against the **learning/test outcome**, not just board cost.
The following per-station scenarios use Australian dollars and a planning
conversion of US$1 = A$1.50, not a live FX quote. Assume 120 two-hour sessions
over three years, an existing host PC, labour at a hypothetical A$100/h and
A$40/year for fixtures/spares. Labour includes setup/qualification/maintenance;
teaching time common to all paths is excluded.

| Path | Initial hardware assumptions | Labour assumption | 3-year incremental TCO | TCO/session |
| --- | --- | ---: | ---: | ---: |
| FeatherWing at proposed US$79 | A$118.50 board + A$60 host + A$75 ELV fixtures = A$253.50 | 6 h = A$600 | A$973.50 | A$8.11 |
| DIY MCP4728 fixture | A$11.25 DAC + A$75 conditioning + A$60 host + A$75 fixtures = A$221.25 | 16 h = A$1,600 | A$1,941.25 | A$16.18 |
| AD3, single-phase V/I only | A$620 instrument + A$75 fixtures = A$695 | 4 h = A$400 | A$1,215 | A$10.13 |
| Eclypse + two AWGs, 3V+1I development | A$1,225 modules/carrier + A$175 supply/cables/conditioning/fixtures allowance = A$1,400 | 16 h = A$1,600 | A$3,120 | A$26.00 |

The AD3 row is not a functional three-phase replacement. For three-phase
observation, budget shared acquisition separately: assume A$700 for a suitable
four-input scope and A$200 for a meter/reference fixture, adding A$900 to each
3V+1I path if not already owned. These are budgeting allowances, not current
equipment quotes or traceable calibration. That gives approximately A$1,874,
A$2,841 and A$4,020 respectively for FeatherWing, DIY and Eclypse paths.
Time-shared equipment lowers cash outlay but reduces simultaneous student
access; fully independent stations multiply acquisition costs.

For a 5 W ELV fixture over 240 hours at an assumed A$0.35/kWh, energy adds only
A$0.42; labour and usable exercises dominate. This estimate excludes PC/scope
energy. Power-HIL is different: at an illustrative 1 kW for 240 hours,
dissipation alone is 240 kWh or A$84, before cooling, safety infrastructure,
calibration and maintenance. Regeneration can reduce consumption but cannot be
assumed without efficiency and idle-power measurements.

The lab case is conditional on firmware reducing setup work. With a one-off
exercise or extensive debugging, the DIY/common-instrument path may be better.
Compare renting/borrowing a qualified power test bench against purchase for
occasional calibration; do not add mains power amplification to this board to
chase an apparent cost saving.

## Appliance/load harnesses in practice and research

These categories solve different problems. Their existence is not evidence
that any one is a turnkey NILM-pretraining appliance.

| Harness or publication | What exists | Suitable role and boundary |
| --- | --- | --- |
| Chroma 63800 [8] | Commercial physical programmable AC load with PF/CF, nonlinear rectifier and inrush modes | Tests actual sources/UPS and load behavior. A named appliance signature may need more than its parametric modes; not ELV. |
| OPAL-RT power-HIL [9] | Real-time simulation plus external power amplifier, feedback and actual power exchange | Closed-loop electrical emulation; amplifier bandwidth, source/sink capability and stability are critical. Not a low-cost DAC replacement. |
| Typhoon HIL404 [7] | Real-time models and many signal-level I/O channels | Controller/sensor-level HIL; external power interface needed for power-HIL. No verified out-of-box NILM appliance library here. |
| "A Power Hardware-In-the-Loop Scheme for Load Emulation Applications", ROPEC 2018 [10] | A published load-emulation scheme | Primary precedent for PHIL load emulation. Bibliographic metadata verified; full text was not accessible, so detailed circuit performance or NILM use is not asserted. |
| "Capturing High-Frequency Harmonic Signatures for NILM: Building a Dataset for Load Disaggregation", Sensors 2025 [11] | Actual scalable acquisition hardware for aggregate and individual appliance measurements | A real measurement/ground-truth harness, not a synthetic appliance power emulator. Essential companion to replay validation. |
| PLAID, Scientific Data 2020 [12] | Recorded voltage/current appliance signatures and measurement methodology | High-frequency waveform source for replay/identification research; a dataset, not an electrical replay rig. |
| WHITED, NILM Workshop 2016 [13] | Measured household/industry startup traces; official v1.1 page documents phase corrections and 1,259 measurements | Transient signature source; preserve version and phase convention. Recordings do not implement hardware emulation. |
| SynD, Scientific Data 2020 [14] | 180 days, 21 appliances, 5 Hz aggregate/submeter power data generated from recorded appliance models | Scheduling, power-profile and low-frequency NILM tests. Does not contain enough waveform detail to reconstruct mains-cycle harmonics uniquely. |
| HiFAKES, 2024 preprint, revised 2025 [15] | Pretrained high-frequency synthetic current-signature generator, labeled aggregates and appliance contributions; generalization methodology | Particularly relevant to synthetic priors/augmentation. Software generator, not proof of DAC replay or real-household accuracy. |
| NILMTK [16] | Open-source NILM evaluation/data tooling | Baselines and reproducible evaluation, not an appliance emulator or turnkey hardware testbed. |

An automated bench of real appliances with synchronized aggregate and per-load
measurement provides genuine signatures and labels, but switching schedules
alone do not emulate every appliance state. Such a bench needs an appropriately
qualified electrical lab; it is not a construction proposal for this ELV design.
Software simulators such as SynD are a cheaper first step for scheduling studies.
Signal replay is the middle ground for testing the meter ADC/firmware path.

## A feasible NILM prior / hardware replay experiment

Proposed, not implemented:

1. Define the task first: appliance/event classification, per-appliance power
   estimation, or slow power-profile disaggregation. Choose sampling bandwidth
   accordingly. Begin with one voltage and one current signature on the ELV
   fixture; reserve three-voltage exercises for phase teaching.
2. Use measured PLAID/WHITED traces and, after checking distribution/model
   licences, HiFAKES-style generated signatures. SynD can schedule duty cycles
   but cannot supply missing high-frequency harmonics. Record dataset/version,
   waveform units, nominal grid voltage/frequency and label definitions.
3. Aggregate currents on a consistent voltage/phase/time base, assign appliances
   to phases explicitly, and preserve per-appliance ground truth. Summing traces
   from incompatible voltage conditions is not physical appliance emulation:
   voltage-dependent loads and shared-source impedance need separate treatment.
4. Pretrain a baseline in software, then replay strictly band-limited ELV
   stimulus through a qualified fixture and capture the actual meter outputs.
   Keep intended waveform, measured waveform and labels separate. Fixed replay
   is open-loop signal injection; call it closed-loop HIL only when measured
   feedback actually affects the real-time synthesis model.
5. Compare digital-only, captured replay and held-out real-household tests using
   event F1, appliance macro-F1, power MAE and energy error. Also measure RMS,
   phase, harmonic amplitudes, clipping, jitter, dropped samples and latency.
   Include equal-power different appliances, overlapping switches, unseen brands,
   background loads, sensor transfer variation and voltage distortion.
6. Split by physical appliance/household before generating variants; keep related
   synthetic seeds and source recordings out of the test set. Freeze deployment
   checkpoints and record training provenance. Test synthetic-only,
   real-only and synthetic-plus-real models; prefer the latter only if the
   held-out real improvement survives uncertainty analysis.

Hardware replay can expose ADC/filter/firmware distortions. It does not
automatically model CT/Rogowski response, mains source impedance, RF emissions,
appliance control loops, household behavior or real-brand diversity. A
domain-specific pretrained prior is realistic; a universal, ready-fitted NILM
network is not supported by this evidence.

Only after demonstrating value should a successor target six independent
channels, simultaneous updates, DMA/buffered streaming, a shared sample clock,
adequate DAC resolution and characterized output conditioning. Set sample
rate from the wanted signal bandwidth and anti-alias/reconstruction requirements;
do not equate a 30 kHz dataset sampling rate with a 30 kHz signal bandwidth.
Keep all development on verified ELV interfaces; no CAD/firmware implementation
or power-stage expansion is included in this assessment.

## Tindie publication handoff

GitHub's README links the original post. On 2026-11-08 the dedicated task browser
still required a Tindie seller login; **no Tindie edit was published**.
[Issue #7](https://github.com/whatnick/Tph_Synth_Featherwing/issues/7) tracks the
pending publication and public-page verification. Preserve current price and
out-of-stock status. Suggested addition to the description:

> Background: the original prototype and energy-monitor testing are described in
> [Simulating 3-phase AC for Energy Monitor testing (October 2017)](https://whatnicklife.blogspot.com/2017/10/simulating-3-phase-ac-for-energy.html).
> Current design files and manufacturing status are on
> [GitHub](https://github.com/whatnick/Tph_Synth_Featherwing).
> The historical prototype results are not certification of the current board.
> This is an ELV signal-level learning/test platform, not a mains power source
> or certified meter calibrator.

## Sources

Product pages/listing checked 2026-11-08. Publisher access failures were resolved
with primary open-access copies or DOI metadata where noted; no unavailable
full-text claims or unverified professional-equipment prices are assumed.

1. [Tindie: 3-phase AC Synthesizer](https://www.tindie.com/products/whatnick/3-phase-ac-synthesizer/), public listing read with browser.
2. [Original prototype blog, October 2017](https://whatnicklife.blogspot.com/2017/10/simulating-3-phase-ac-for-energy.html). The legacy DIYODE link returned 404 during this check.
3. [Adafruit MCP4728 product 4470](https://www.adafruit.com/product/4470), prices and technical specifications.
4. [Digilent Analog Discovery 3](https://digilent.com/shop/analog-discovery-3/), A$620, two AWG channels.
5. [Digilent Eclypse Z7](https://digilent.com/shop/eclypse-z7/), A$875 carrier.
6. [Digilent Zmod AWG 1411](https://digilent.com/shop/zmod-awg-1411-2-channel-14-bit-arbitrary-waveform-generator-awg-module/), A$175 module and technical specifications.
7. [Typhoon HIL404](https://www.typhoon-hil.com/products/hil-simulator/hil404/), hardware I/O and simulator specification.
8. [Chroma 63800](https://www.chromausa.com/product/programmable-ac-electronic-load-63800/), physical load modes, voltage/power limits; quotation required.
9. [OPAL-RT power-HIL](https://www.opal-rt.com/industries-and-applications/simulation-and-testing/power-hardware-in-the-loop/), amplifier/feedback architecture.
10. [ROPEC 2018 load-emulation scheme, DOI 10.1109/ROPEC.2018.8661394](https://doi.org/10.1109/ROPEC.2018.8661394), title/year verified using Crossref; full-text details not assessed.
11. [Sensors 2025, DOI 10.3390/s25154601](https://doi.org/10.3390/s25154601); [open-access copy](https://pmc.ncbi.nlm.nih.gov/articles/PMC12349275/), abstract verified through Europe PMC.
12. [PLAID paper, DOI 10.1038/s41597-020-0389-7](https://doi.org/10.1038/s41597-020-0389-7); [open-access copy](https://pmc.ncbi.nlm.nih.gov/articles/PMC7015894/), title/year verified through Crossref and Europe PMC.
13. [WHITED official TUM dataset page](https://www.cs.cit.tum.de/dis/resources/whited/), includes original paper link and v1.1 corrections.
14. [SynD paper, DOI 10.1038/s41597-020-0434-6](https://doi.org/10.1038/s41597-020-0434-6); [open-access copy](https://pmc.ncbi.nlm.nih.gov/articles/PMC7118146/), methods read through Europe PMC full-text XML.
15. [HiFAKES, arXiv:2409.00062v2](https://arxiv.org/html/2409.00062v2), Kamyshev, Moghimian and Ouerdane; 2024 preprint revised 2025; [DOI](https://doi.org/10.48550/arXiv.2409.00062).
16. [NILMTK source and documentation](https://github.com/nilmtk/nilmtk).

Local cost/architecture evidence: `Tph_Synth_Featherwing.kicad_sch`,
`manufacturing/v0.4/assembly/assembly-bom-REVIEW-ONLY.csv`,
`sourcing/distributor-review-2026-11-07.json`,
`sourcing/distributor-review-substitutions-2026-11-07.json`, and
`manufacturing/elecrow-pcba-2026-11-07/quote.json`.
