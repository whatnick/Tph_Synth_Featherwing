3-Phase Synth FeatherWing v0.4 manufacturing preparation

STATUS: Fabrication files prepared; ASSEMBLY/PURCHASING ON HOLD.
This is not approval to manufacture or order components.
Nominal outline: 51.0 x 58.5 mm; 2 copper layers; 1.6 mm board.
Confirm FR-4, copper weight, finish, quantity and panelization before an order.

Bare-board archive: Tph_Synth_Featherwing-v0.4-fabrication.zip
Contains fresh Gerbers and separate PTH/NPTH drills only (plus job file if emitted).
Drill maps and checks remain outside the upload archive.
Do not use the historical Tph_Synth_Featherwing\gerbers or bom folders.

assembly\assembly-bom-REVIEW-ONLY.csv is NOT an approved purchasing BOM.
C1-C3, C4-C11/C18 and C12 use approved breakout replacements; hardware validation remains required.
R10 needs exact mechanical/pin verification. Feather host headers are intentionally DNP, not a factory release blocker.
See assembly\distributor-review-*.json for dated MCP stock, lifecycle and packaging evidence.
TDK 22uF replacements are sourced through LCSC/JLCPCB; verify exact MPN supply before ordering.
All legacy MPNs still require electrical/mechanical qualification and a fresh stock check before ordering.
MS1 is the external host; no adapter PCB is fitted to this PCB at MS1.
DO NOT FIT Feather host 12-pin/16-pin headers at manufacture; excluded from purchasing BOM.
Users fit compatible stacking headers to suit their Feather after manufacture. J2/J3 remain fitted.
JP1/JP2, test pads and the OSHW logo are PCB features, not purchased components.

positions-smt.csv covers SMT only; THT parts are listed in release-status.json.
Gerbers/drills/positions use absolute CAD origin, millimetres; bottom X is not negated.
Back assembly SVG is mirrored for viewing only. Confirm machine rotations and polarity.
Unvalidated hardware: power rails, host I2C/firmware, DAC and analog/current outputs.
See release-status.json for blockers and manifest.json for source/output SHA-256 hashes.
